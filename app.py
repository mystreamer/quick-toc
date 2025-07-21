from bottle import run, route, request, response
from script import main
from types import SimpleNamespace

@route('/', method='GET')
def generate_form():
    return '''
        <form action="/" method="post" enctype="multipart/form-data">
            Select PDF: <input type="file" name="pdf" accept="application/pdf" required><br>
            Start Page: <input type="number" name="start_page" required><br>
            End Page: <input type="number" name="end_page" required><br>
            Offset: <input type="number" name="page_offset" value="0"><br>
            <input type="submit" value="Submit">
        </form>
        '''

@route('/', method='POST')
def process_document():
    # Get form data
    sp = int(request.POST.start_page)
    ep = int(request.POST.end_page)
    po = int(request.POST.page_offset)
    pf =  request.files.get('pdf')

    args_dict = {
        "input" : pf.file,
        # "output" : "output.pdf",
        "start_page" : sp,
        "end_page" : ep,
        "page_offset" : po,
    }

    args = SimpleNamespace(**args_dict)

    # Call main method
    annotated_file = main(
        args
    )

    # Set appropriate headers
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f"attachment; filename={ strip_pdf_extension(pf.filename) + "_toc" }.pdf"

    return annotated_file.getvalue()

# helpers
def strip_pdf_extension(filename):
    if filename.endswith(".pdf"):
        filename = filename[:-4]
        return filename
    return filename

if __name__ == '__main__':
    run(host='localhost', port=8055, debug=True, reloader=True)
