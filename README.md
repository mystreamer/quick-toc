quick-toc
-------------------------------------------------------------------------

Quick-toc allows you to quickly add a table of contents to your PDF files.

## Setup

Set your OpenAI API key in the environment variable with `export OPENAI_API_KEY=...`

Using the nix package manager, or on a nixOS system, cd to this directory and run:

```
nix-shell
```

## Usage

### Web App

Run: `python app.py`

### Command Line Interface

To add a table of contents to a PDF file, run:

```

python script.py test/input/book2.pdf book2_outl.pdf --start_page=7 --end_page=12 --page_offset=0

```

**Parameters**:

- `input_file`: The input PDF file to add a table of contents to.
- `output_file`: The output PDF file to save the table of contents to.
- `start_page`: The page number to start the table of contents from.
- `end_page`: The page number to end the table of contents at.
- `page_offset`: The page number to offset the table of contents by.
