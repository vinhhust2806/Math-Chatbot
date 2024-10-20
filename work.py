from st_pages import Page, show_pages, add_page_title


if __name__ == "__main__":
 
 add_page_title()     
 show_pages(
        [
            Page("main.py", "Math Question", "🏠"),
            Page("ocr.py", "OCR Image", "📒"),
            Page("equation.py", "Equation", "🔥"),
        ])


 