class BaseConverter:
    def base_converter(self, input_file: str, output_extension: str) -> None:
        raise NotImplementedError("Subclasses must implement this method")