import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def list_entries():
    """ Returns a list of all encyclopedia entry names. """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(
        re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")
    ))

def save_entry(title, content):
    """ Saves an encyclopedia entry in Markdown format.
        If an entry with the same title exists, it replaces the old one.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    try:
        with open(f"entries/{title}.md", "rb") as f:
            return f.read().decode("utf-8", errors="replace")  # Replaces invalid characters
    except UnicodeDecodeError:
        return "Error loading entry: Encoding issue detected!"

