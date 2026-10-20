"""Validasi input dari klien."""


def validate_task_payload(data, max_title, max_description, partial=False):
    """Mengembalikan (data_bersih, daftar_error)."""
    errors = []
    cleaned = {}

    if not isinstance(data, dict):
        return {}, ["Body harus berupa objek JSON"]

    if "title" in data or not partial:
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append("title wajib diisi dan berupa teks")
        elif len(title.strip()) > max_title:
            errors.append(f"title maksimal {max_title} karakter")
        else:
            cleaned["title"] = title.strip()

    if "description" in data:
        desc = data["description"]
        if not isinstance(desc, str):
            errors.append("description harus berupa teks")
        elif len(desc) > max_description:
            errors.append(f"description maksimal {max_description} karakter")
        else:
            cleaned["description"] = desc.strip()

    if "done" in data:
        if not isinstance(data["done"], bool):
            errors.append("done harus berupa boolean")
        else:
            cleaned["done"] = data["done"]

    return cleaned, errors


def parse_bool_param(value):
    """Ubah query string 'true'/'false' menjadi bool, selain itu None."""
    if value is None:
        return None
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None
