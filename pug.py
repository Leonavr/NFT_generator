import os
import random

from PIL import Image, ImageDraw, ImageChops
import colorsys


class Pug:
    def __init__(self):
        self.pug = Image.open('new nft/pig.png')

    def hat_on_pug(self):
        pug = self.pug.convert("RGBA")
        size = pug.size

        path = 'new_hats'
        all_pigs = []
        for file in os.walk(path):
            for f in file[-1]:
                if 'doctor' in f:
                    hat = Image.open(f"new_hats/{f}")
                    hat = hat.convert("RGBA")
                    pug.thumbnail(size, Image.Resampling.LANCZOS)
                    final_thumb = Image.new(
                        mode='RGBA', size=size, color=(random.randint(0, 255),
                                                       random.randint(0, 255),
                                                       random.randint(0, 255))
                    )
                    final_thumb = Image.alpha_composite(final_thumb, pug)
                    intermediate = Image.alpha_composite(final_thumb, hat)

                    all_pigs.append(intermediate)

        return all_pigs

    @staticmethod
    def random_color():
        h = random.random()
        s = 1
        v = 1

        float_rgb = colorsys.hsv_to_rgb(h, s, v)
        rgb = [int(x * 255) for x in float_rgb]
        return tuple(rgb)

    def generate_back_for_pug(self):
        self.image_bg_color = self.random_color()
        images = self.hat_on_pug()
        new_images = []
        for img in images:
            datas = img.getdata()
            # new_image_data = []
            # new_image_data.append(self.image_bg_color)
            # -*- coding: utf-8 -*-
            newImage = []
            for item in img.getdata():
                if item[:3] == (255, 255, 255):
                    newImage.append((255, 255, 255, 0))
                else:
                    newImage.append(item)

            img.putdata(self.image_bg_color)
            new_images.append(img)
        # image = self.overlay_canvas(image, start_color, end_color)
        #
        # image = image.resize((self.target_size_px, self.target_size_px),
        #                      resample=Image.Resampling.LANCZOS)
        return new_images


if __name__ == "__main__":
    generator = Pug()

    images = generator.generate_back_for_pug()
    # images[0].save(f"pig_nft/pig_0.png")

    for index, img in enumerate(images):
        img.save(f"pig_nft_2/pig_2_{index}.png")
