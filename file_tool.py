"""
File tool: copies or moves a document to a destination folder.
"""

import os
import shutil


def save_document(
    source_path: str,
    destination_folder: str,
    new_filename: str = None,
    move: bool = False
) -> dict:
    """
    Copy (or move) a document to a destination folder.

    Args:
        source_path:         Absolute path to the source file.
        destination_folder:  Absolute path to the target folder.
        new_filename:        Optional new filename. If None, keeps original name.
        move:                If True, move instead of copy.

    Returns:
        Dict with status and final saved path.
    """
    if not os.path.isfile(source_path):
        return {"error": f"Source file not found: {source_path}"}

    os.makedirs(destination_folder, exist_ok=True)

    filename = new_filename if new_filename else os.path.basename(source_path)
    dest_path = os.path.join(destination_folder, filename)

    try:
        if move:
            shutil.move(source_path, dest_path)
            action = "moved"
        else:
            shutil.copy2(source_path, dest_path)
            action = "copied"
    except Exception as e:
        return {"error": f"Failed to {('move' if move else 'copy')} file: {e}"}

    return {
        "status": "success",
        "action": action,
        "saved_path": dest_path,
        "filename": filename,
    }
