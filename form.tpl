<html>
    <head>
        <title>QuickTOC: LLM-based Table of Contents Generator</title>
        <!-- Add style.css -->
        <link rel="stylesheet" type="text/css" href="static/style.css">
    </head>
    <body>
        <!-- Add the logo.png -->
        <img src="static/logo.png" alt="Logo" width="200" height="200">
        <details>
            <summary>About 💡</summary>
            <div class="accordion">
                <p>
                    This web-app allows you to quickly add a table of contents to your PDF. The download should start automatically once you click on the submit button.
                </p>
            </div>
        </details>
        <form  action="/" method="post" enctype="multipart/form-data">
            <label for="pdf">Select PDF:</label>
            <input type="file" name="pdf" accept="application/pdf" required><br>
            <label for"start_page">Start Page:</label>
            <input type="number" name="start_page" required><br>
            <label for"end_page">End Page:</label>
            <input type="number" name="end_page" required><br>
            <label for"page_offset">Page Offset:</label>
            <input type="number" name="page_offset" value="0"><br>
            <input type="submit" value="Submit">
        </form>
        <details>
            <summary>❓ Help</summary>
            <div class="accordion">
                        <p><strong>📄 What file types can I upload?</strong><br>
            Currently, only PDF files are supported. Make sure your file ends with <code>.pdf</code>.</p>

            <p><strong>📅 What do "Start Page" and "End Page" mean?</strong><br>
            These two parameters indicate when the Terms of Content starts and when it ends. Use your PDF viewer to provide this delimitation.</p>

            <p><strong>➕ What is the "Offset" for?</strong><br>
            Offset indicates the discrepancy between the book page numbering and the PDF page numbering. To figure out the offset go to a page that has a number written on it and then compare this with the page number provided by the provided PDF viewer. Then subtract the book-indicated page number from the PDF page number. Normally, PDF-page-number > book-page-number, so this should be a non-negativeinteger.</p>
        </details>
    </body>
</html>
