from PIL import Image, ImageFile, ImageEnhance, ImageFilter, ImageOps
import click


def load_image(file_path: str):
    try:
        image = Image.open(file_path)
        image.load()
        return image
    except Exception as e:
        raise IOError(f"Error opening image file: {e}")


def save_image(image: ImageFile.ImageFile, file_path: str):
    try:
        image.save(file_path)
    except Exception as e:
        raise IOError(f"Error saving image file: {e}")


def resize_image(image: ImageFile.ImageFile, width=0, height=0):
    try:
        if width == 0 and height == 0:
            return image

        original_width, original_height = image.size

        if width == 0:
            # Calculate width to maintain aspect ratio
            aspect_ratio = original_width / original_height
            width = int(height * aspect_ratio)
        elif height == 0:
            # Calculate height to maintain aspect ratio
            aspect_ratio = original_height / original_width
            height = int(width * aspect_ratio)

        resized_image = image.resize((width, height))
        return resized_image
    except Exception as e:
        raise IOError(f"Error resizing image file: {e}")


def rotate_image(image: ImageFile.ImageFile, angle=0.0):
    try:
        if angle == 0:
            return image

        rotated_image = image.rotate(angle=angle, expand=True)
        return rotated_image
    except Exception as e:
        raise IOError(f"Error rotating image file: {e}")


def apply_filter(image: ImageFile.ImageFile, filter_name: str):
    try:
        image_filter_options = [
            "BLUR",
            "CONTOUR",
            "DETAIL",
            "EDGE_ENHANCE",
            "EDGE_ENHANCE_MORE",
            "EMBOSS",
            "FIND_EDGES",
            "SHARPEN",
            "SMOOTH",
            "SMOOTH_MORE",
            "GRAYSCALE",
        ]
        if filter_name not in image_filter_options:
            raise IOError("Sorry, this is not a valid filter name")

        if filter_name == "GRAYSCALE":
            new_image = ImageOps.grayscale(image)
        else:
            new_image = image.filter(ImageFilter[filter_name])

        return new_image
    except Exception as e:
        raise IOError(f"Error applying filter to the image: {e}")


def adjust_brightness(image: ImageFile.ImageFile, factor: float = 1.0):
    try:
        image_brightness_enhancer = ImageEnhance.Brightness(image)
        new_image = image_brightness_enhancer.enhance(factor=factor)
        return new_image
    except Exception as e:
        raise IOError(f"Error enhancing brightness of the image: {e}")


def adjust_contrast(image: ImageFile.ImageFile, factor: float = 1.0):
    try:
        image_contrast_enhancer = ImageEnhance.Contrast(image)
        new_image = image_contrast_enhancer.enhance(factor=factor)
        return new_image
    except Exception as e:
        raise IOError(f"Error enhancing contrast of the image: {e}")


def crop_image(
    image: ImageFile.ImageFile, left: float, top: float, right: float, bottom: float
):
    try:
        original_width, original_height = image.size
        if (
            left == 0
            and right == original_width
            and top == 0
            and bottom == original_height
        ):
            return image

        if left > right:
            raise IOError("Invalid Dimensions: Left cannot be greater than right")
        if top > bottom:
            raise IOError("Invalid Dimensions: Top cannot be greater than bottom")

        new_image = image.crop((left, top, right, bottom))
        return new_image
    except Exception as e:
        raise IOError(f"Error cropping image: {e}")


@click.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.argument("output_path", type=click.Path())
@click.option(
    "--resize", nargs=2, type=int, help="Resize the image. Usage: --resize WIDTH HEIGHT"
)
@click.option("--rotate", type=float, help="Rotate the image by given angle")
@click.option(
    "--filter",
    "filter_name",
    type=click.Choice(
        [
            "BLUR",
            "CONTOUR",
            "DETAIL",
            "EDGE_ENHANCE",
            "EDGE_ENHANCE_MORE",
            "EMBOSS",
            "FIND_EDGES",
            "SHARPEN",
            "SMOOTH",
            "SMOOTH_MORE",
            "GRAYSCALE",
        ]
    ),
    help="Apply a filter to the image",
)
@click.option(
    "--brightness",
    type=float,
    help="Adjust brightness. Values > 1 brighten, < 1 darken",
)
@click.option(
    "--contrast", type=float, help="Adjust contrast. Values > 1 increase, < 1 decrease"
)
@click.option(
    "--crop",
    nargs=4,
    type=int,
    help="Crop the image. Usage: --crop LEFT TOP RIGHT BOTTOM",
)
def main(
    input_path, output_path, resize, rotate, filter_name, brightness, contrast, crop
):
    # Load the image
    image = load_image(input_path)

    # Apply operations based on provided options
    if resize:
        image = resize_image(image, resize[0], resize[1])
    if rotate:
        image = rotate_image(image, rotate)
    if filter_name:
        image = apply_filter(image, filter_name)
    if brightness:
        image = adjust_brightness(image, brightness)
    if contrast:
        image = adjust_contrast(image, contrast)
    if crop:
        image = crop_image(image, crop[0], crop[1], crop[2], crop[3])

    # Save the resulting image
    save_image(image, output_path)
    click.echo(f"Image saved to {output_path}")


if __name__ == "__main__":
    main()
