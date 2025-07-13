import re
from utils import logger

def convert_text_to_html(text: str) -> str:
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    
    def build_file_link(urlfilepath: str) -> str:
        splitpath = urlfilepath.split('|')
        filename = splitpath[-1]
        filename = filename.split('?')[0]
        url = '/'.join(splitpath)
        # logger.info(f"url: {url}")
        return f'<a href="{url}">{filename}</a>'
    
    def process_paragraph(para: str) -> str:
        lines = para.strip().split("\n")
        result = []
        in_list = False

        for line in lines:
            stripped = line.strip()
            
            # source lines
            match = re.match(r"(Zdroj|Zdroje|Source|Sources):\s*(.+)", stripped)
            if match:
                _, source_text = match.groups()
                files = re.split(r",\s", source_text)
                linked_files = []
                for f in files:
                    file_link = f"<li>{build_file_link(f)}</li>"
                    linked_files.append(file_link)
                    
                logger.info(f"linked files: {linked_files}")
                result.append(f"<p>{"Zdroje:" if len(linked_files) > 1 else "Zdroj:"}</p>")
                result.append(f"<ul>")
                for lf in linked_files:
                    result.append(lf) 
                result.append(f"</ul>")
                continue
            
            # unordered list
            if stripped.startswith("-"):
                if not in_list:
                    result.append("<ul>")
                    in_list = True
                result.append(f"<li>{stripped[1:].strip()}</li>")
            else:
                if in_list:
                    result.append("</ul>")
                    in_list = False
                if stripped:
                    result.append(f"<p>{stripped}</p>")
        if in_list:
            result.append("</ul>")
        return ''.join(result)


    # Split text into paragraphs by double newlines
    paragraphs = text.strip().split("\n\n")
    html_parts = [process_paragraph(p) for p in paragraphs if p.strip()]
    return ''.join(html_parts)
