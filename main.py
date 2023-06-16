from PIL import Image


def encrypt(msg, img):
    max_width, max_height = img.size
    width = 1
    height = 0
    bits = []

    length = len(msg)*8
    img.putpixel((0, 0), (length // (256 * 256), length // 256 % 256, length % 256))

    for symbol in msg:
        symbol_bits = []
        for i in range(8):
            symbol_bits.insert(0, ((ord(symbol) >> i) & 1))
        bits += symbol_bits

    #print(bits)
    while len(bits) % 3 != 0:
        bits.append(2)
    for i in range(0, len(bits), 3):
        r, g, b = img.getpixel((width, height))

        r = (bits[i] | (r >> 1 << 1))
        g = (bits[i+1] | (g >> 1 << 1))
        b = (bits[i+2] | (b >> 1 << 1))

        img.putpixel((width, height), (r, g, b))

        if width == max_width and height == max_height:
            print("not enough pixels")
            return 0
        if width < max_width:
            width += 1
        else:
            height += 1
            width = 0

    img.save("encryptedImage.png")
    return 1


def decrypt(img):
    msg = ""
    max_width, max_height = img.size
    width = 1
    height = 0
    bits = []
    r, g, b = img.getpixel((0, 0))
    length = r * 256 * 256 + g * 256 + b
    while len(bits) < length:
        r, g, b = img.getpixel((width, height))

        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

        if width < max_width:
            width += 1
        else:
            height += 1
            width = 0

    for i in range(length//8):
        symbol = bits[i*8:i*8+8]
        for b in getbytes(iter(symbol)):
            if b != 0:
                msg += chr(b)
    return msg


def getbytes(bits):
    done = False
    while not done:
        byte = 0
        for _ in range(0, 8):
            try:
                bit = next(bits)
            except StopIteration:
                bit = 0
                done = True
            byte = (byte << 1) | bit
        yield byte


def main():
    img = Image.open("image.jpg")
    msg = input("Enter message: ")
    info = encrypt(msg, img)
    if info == 1:
        print("The message was successfully encrypted into an image encryptedImage.png!")
    else:
        print("Oops! Something went wrong!!!")

    img = Image.open("encryptedImage.png")
    encrypted_msg = decrypt(img)
    print(f"Decrypted message: {encrypted_msg}")


if __name__ == '__main__':
    main()

