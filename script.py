# #!/usr/bin/env python3
# coding: utf-8
import argparse
import os
import io
from openai import OpenAI
from pydantic import BaseModel
from pikepdf import Pdf, OutlineItem
from pdf2image import convert_from_bytes
from PIL import Image
import pprint
import base64

def pprint_dict(dict_data):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(dict_data)

class PageReference(BaseModel):
    # model_config = ConfigDict(extra='forbid')  # required for openai
    title: str
    page_number: int

class Outline(BaseModel):
    # model_config = ConfigDict(extra='forbid')  # required for openai
    items: list[PageReference]

def convert_pil_to_png(image):
    buff = io.BytesIO()
    image.save(buff, "png")
    img = Image.open(buff)
    # import pdb; pdb.set_trace()
    # image.save("test/test_img.png", "png")
    encoded_image = base64.b64encode(buff.getvalue()).decode('utf-8')
    return encoded_image

def load_and_resize_image(image, max_size=1024):
    """
    Load and resize an image while maintaining aspect ratio
    """
    # image = Image.open(image_path)

    # Get current dimensions
    width, height = image.size

    # Calculate scaling factor
    scale = min(max_size / width, max_size / height)

    # Only resize if image is larger than max_size
    if scale < 1:
        new_width = int(width * scale)
        new_height = int(height * scale)
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return image

def convert_pdf_to_image(pdf_path):
    # images = convert_from_path(pdf_path)
    images = convert_from_bytes(pdf_path.getvalue())
    return images

def extract_pages_from_pdf(pdf_path, start_page, end_page):
    pdf = Pdf.open(pdf_path)
    outline = Pdf.new()
    extracted_outline = [pdf.pages[p] for p in range(start_page - 1, end_page)]
    [outline.pages.append(page) for page in extracted_outline]
    buff = io.BytesIO()
    # outline.save("test/output/extracted_outline.pdf")
    outline.save(buff)
    return buff

def add_outline(input_path, parsed_outline, page_offset: int):
    pdf = Pdf.open(input_path)
    with pdf.open_outline() as outline:
        outline.root.extend([
            *[OutlineItem(o.title, o.page_number + page_offset - 1) for o in parsed_outline.items]
            ])
    out_buffer = io.BytesIO()
    # pdf.save(output_path)
    pdf.save(out_buffer)
    return out_buffer

def main(args):
    img_buff = extract_pages_from_pdf(
            args.input,
            args.start_page,
            args.end_page
            )

    images = convert_pdf_to_image(img_buff)
    images_resized = [load_and_resize_image(image) for image in images]
    images_resized_json = [{ "type" : "input_image" , "image_url" : f"data:image/png;base64,{  convert_pil_to_png(img) }" } for img in images_resized]

    client = OpenAI(
            # "gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
            )

    resp = client.responses.parse(
             # model = "gpt-4o",
             model = "gpt-4o-mini",
             input = 
             [
                 {"role": "system", "content": "Extract the event information."},
                     {
                         "role": "user", 
                         "content": [
                                 *images_resized_json,
                                 {
                                     "type": "input_text",
                                     "text": "Above you are given photos of the table of contents of a book (in sequential order; i.e. first image first page of the table of contents). Please convert this table of contents into a single list adhering to the following JSON-schema: { Outline.model_json_schema() }"
                                 }
                             ]
                          },
                     ],
             text_format = Outline 
             )

    ret_pdf_buf = add_outline(args.input, resp.output_parsed, args.page_offset)
    return ret_pdf_buf

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='quick-toc', description='Quickly add a table of contents to your PDF')
    parser.add_argument('input', type=str, help='Path to input PDF')
    parser.add_argument('output', type=str, help='Path to output PDF')
    parser.add_argument('--start_page', type=int, help='Starting page number')
    parser.add_argument('--end_page', type=int, help='Ending page number')
    parser.add_argument('--page_offset', type=int, default=0, help='Absolute difference between page number on ToC and in PDF')
    args = parser.parse_args()

    ###### CONSTRAINTS ######
    max_pages_outline = 5
    assert args.end_page > args.start_page, "End page must be greater than start page"
    assert (args.end_page - args.start_page + 1) <= max_pages_outline, f"End page must be within {max_pages_outline} pages of start page"

    ret_buf = main(args)

    with open(args.output, "wb") as f:
        f.write(ret_buf.getvalue())


