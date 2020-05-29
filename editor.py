from simpleimage import SimpleImage
from tkinter import filedialog as fd
from PIL import Image
import PIL

BLUR_SIZE = 3   # Size of the box filter. Should be positive odd integer
BLUR_ITER = 6   # Number of iterations of box filtering.


def main():
    # This is a program that performs several actions on an image file.
    file_types = [('JPG files', '*.jpg'), ('PNG files', '*.png'), ('All files', '*.*')]
    filename = get_file(file_types)
    image = SimpleImage(filename)
    width = image.width
    height = image.height

    selection = int(input("Please select a function:\n1. Rotate\n2. Flip\n3. Sepia\n4. Negative\n"
                          "5. Grayscale\n6. Pencil Sketch\n7. Blur image\n8. Brightness\n9. Contrast\n"
                          "10. Solarise\n11. Gamma correction\n"))

    if selection == 1:

        option = int(input("Would like to rotate:\n1. 90° clockwise.\n2. 90° anticlockwise.\n3. 180° rotation.\n"))
        while 0 > option > 3:
            option = int(input("Would like to rotate:\n1. 90° clockwise.\n2. 90° anticlockwise.\n3. 180° rotation.\n"))
        final_img = rotate_image(image, width, height, option)

    if selection == 2:

        option = int(input("Would like to flip:\n1. Vertically.\n2. Horizontally.\n"))
        while 0 > option > 2:
            option = int(input("Would like to flip:\n1. Vertically.\n2. Horizontally.\n"))
        option = int(input("Would like to flip:\n1. Vertically.\n2. Horizontally.\n"))
        final_img = flip_image(image, width, height, option)

    if selection == 3:
        final_img = sepia(image)

    if selection == 4:
        final_img = negative(image)

    if selection == 5:
        final_img = gray_scale(image)

    if selection == 6:
        final_img = pencil(image)

    if selection == 7:
        final_img = blur(image, BLUR_ITER, BLUR_SIZE)

    if selection == 8:
        level = int(input("Choose a brightness value in the range of -255 to +255:\n"))
        final_img = brighter(image, level)

    if selection == 9:
        level = int(input("Choose a contrast value in the range of -255 to +255:\n"))
        final_img = contrast_adjustment(image, level)

    if selection == 10:
        level = int(input("Choose a preferred colour threshold in the range of -255 to +255:\n"))
        final_img = solarise(image, level)

    if selection == 11:
        gamma = float(input("Choose a value for gamma, preferably between 0.01 and 7.99:\n"))
        final_img = gamma_correction(image, gamma)

    Image.save()

    final_img.show()


def flip_image(image, width, height, option):
    flip_img = SimpleImage.blank(width, height)
    if option == 1:
        for x in range(width):
            for y in range(height):
                pixel = image.get_pixel(x, y)
                flip_img.set_pixel(x, (height - (y + 1)), pixel)
    else:
        for x in range(width):
            for y in range(height):
                pixel = image.get_pixel(x, y)
                flip_img.set_pixel(width - (x + 1), y, pixel)

    return flip_img


def rotate_image(image, width, height, option):
    if option == 1:
        rot_img = SimpleImage.blank(height, width)
        for x in range(width):
            for y in range(height):
                pixel = image.get_pixel(x, y)
                rot_img.set_pixel(height - (y + 1), x, pixel)

    if option == 2:
        rot_img = SimpleImage.blank(height, width)
        for x in range(width):
            for y in range(height):
                pixel = image.get_pixel(x, y)
                rot_img.set_pixel(y , width - (x + 1), pixel)

    if option == 3:
        rot_img = SimpleImage.blank(width, height)
        for x in range(width):
            for y in range(height):
                pixel = image.get_pixel(x, y)
                rot_img.set_pixel(width - (x + 1), height - (y + 1), pixel)

    return rot_img


def negative(image):
    for pixel in image:
        pixel.red = 255 - pixel.red
        pixel.blue = 255 - pixel.blue
        pixel.green = 255 - pixel.green

    return image


def sepia(image):
    for pixel in image:

        pixel.red = pixel.red * 0.393 + pixel.green * 0.769 + pixel.blue * 0.189
        pixel.blue = pixel.red * 0.272 + pixel.green * 0.534 + pixel.blue * 0.131
        pixel.green = pixel.red * 0.349 + pixel.green * 0.686 + pixel.blue * 0.168

    return image


def gray_scale(image):
    for pixel in image:
        value = 0.299 * pixel.red + 0.587 * pixel.green + 0.114 * pixel.blue
        pixel.red = value
        pixel.green = value
        pixel.blue = value

    return image


def pencil(image):
    gray = gray_scale(image)
    gray_copy = copy_image(gray)
    inverted = negative(gray)
    blurred = blur(inverted, BLUR_ITER, BLUR_SIZE)
    for px in gray_copy:
        x = px.x
        y = px.y
        px_top = gray_copy.get_pixel(x,y)
        px_bottom = blurred.get_pixel(x,y)
        px.red = compute_dodge(px_top.red, px_bottom.red)
        px.green = compute_dodge(px_top.green, px_bottom.green)
        px.blue = compute_dodge(px_top.blue, px_bottom.blue)

    return gray_copy


def compute_dodge(top_val, bottom_val):
    val = bottom_val * 255 / max(1, 255 - top_val)
    return min(val, 255)


def blur(image, num_iter, blur_size):
    reference_img = image
    for i in range(num_iter):
        blurred = copy_image(reference_img)
        for x in range(reference_img.width):
            for y in range(reference_img.height):
                red = 0
                blue = 0
                green = 0
                count = 0
                r = (blur_size - 1) // 2
                for j in range(x - r, x + r + 1):
                    for k in range(y - r, y + r + 1):
                        if 0 <= j < reference_img.width and 0 <= k < reference_img.height:
                            count += 1
                            px = reference_img.get_pixel(j, k)
                            red += px.red
                            blue += px.blue
                            green += px.green
                pixel = blurred.get_pixel(x, y)
                pixel.red = red / count
                pixel.green = green / count
                pixel.blue = blue / count
        reference_img = blurred

    return blurred


def brighter(image, level):
    for pixel in image:
        pixel.red += level
        pixel.green += level
        pixel.blue += level
    return image


def contrast_adjustment(image, contrast):
    factor = (259 * (contrast + 255)) / (255 * (259 - contrast))
    for pixel in image:
        pixel.red = factor * (pixel.red - 128) + 128
        pixel.green = factor * (pixel.green - 128) + 128
        pixel.blue = factor * (pixel.blue - 128) + 128
    return image


def solarise(image, threshold):
    for pixel in image:
        if pixel.red < threshold:
            pixel.red = 255 - pixel.red
        if pixel.green < threshold:
            pixel.green = 255 - pixel.green
        if pixel.blue < threshold:
            pixel.blue = 255 - pixel.blue

    return image


def gamma_correction(image, gamma):
    gammacorrection = 1 / gamma
    for pixel in image:
        pixel.red = 255 * ((pixel.red / 255) ** gammacorrection)
        pixel.green = 255 * ((pixel.green / 255) ** gammacorrection)
        pixel.blue = 255 * ((pixel.blue / 255) ** gammacorrection)
    return image


def get_file(files):
    filename = fd.askopenfilename(initialdir="/", filetypes=files)
    return filename


def copy_image(image): # Creates a copy of the image
    copy = SimpleImage.blank(image.width, image.height)
    for pixel in copy:
        x = pixel.x
        y = pixel.y
        copy.set_pixel(x, y, image.get_pixel(x, y))
    return copy


if __name__ == "__main__":
    main()
