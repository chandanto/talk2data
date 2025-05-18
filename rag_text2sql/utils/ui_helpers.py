import base64

def get_base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def format_documents(docs):
    if not docs:
        return "No relevant documents found."
    result = ""
    for doc in docs:
        meta = doc.metadata
        result += f"\n**Source:** {meta.get('source', 'Unknown')} (Page {meta.get('page_number', 'N/A')})\n```\n{doc.page_content.strip()}\n```\n"
    return result.strip()
