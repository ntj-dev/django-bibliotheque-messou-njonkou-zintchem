class ConvertisseurISBN:
    regex = "[0-9]{3}-[0-9]{1}-[0-9]{4}-[0-9]{4}-[0-9]{1}"

    def to_python(self, value):
        return value.replace("-", "")

    def to_url(self, value):
        return value