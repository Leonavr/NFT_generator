import random

from PIL import Image, ImageDraw, ImageChops
import colorsys


class NftGenerator:
    def __init__(self):
        self.target_size_px = 1400
        self.scale_factor = 2
        self.image_size_px = self.target_size_px * self.scale_factor
        self.padding_px = 12 * self.scale_factor
        self.image_bg_color = (0, 0, 0)
        self.points = []

    @staticmethod
    def random_color():
        h = random.random()
        s = 1
        v = 1

        float_rgb = colorsys.hsv_to_rgb(h, s, v)
        rgb = [int(x*255) for x in float_rgb]
        return tuple(rgb)

    def interpolate(self, start_color, end_color, factor: float):
        recip = 1 - factor
        return(
            int(start_color[0] * recip + end_color[0] * factor),
            int(start_color[1] * recip + end_color[1] * factor),
            int(start_color[2] * recip + end_color[2] * factor)
        )

    def points_generator(self):
        for i in range(60):
            random_point = (
                random.randint(self.padding_px, self.image_size_px-self.padding_px),
                random.randint(self.padding_px, self.image_size_px-self.padding_px)
            )
            self.points.append(random_point)

    def center_the_image(self):
        min_x = min([p[0] for p in self.points])
        max_x = max([p[0] for p in self.points])

        min_y = min([p[1] for p in self.points])
        max_y = max([p[1] for p in self.points])

        # Center the image
        delta_x = min_x - (self.image_size_px - max_x)
        delta_y = min_y - (self.image_size_px - max_y)
        for i, point in enumerate(self.points):
            self.points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)

    def draw_line(self, image, overlay_image, coordinates, thickness, line_color):
        overlay_draw = ImageDraw.Draw(overlay_image)
        overlay_draw.line(coordinates, width=thickness, fill=line_color, joint='curve')

        x, y = 512, 512
        eX, eY = 256, 256
        bbox = (x / 2 - eX / 2, y / 2 - eY / 2, x / 2 + eX / 2, y / 2 + eY / 2)

        # overlay_draw.ellipse(bbox, outline=line_color, width=10)

        image = ImageChops.add(image, overlay_image)
        return image

    def overlay_canvas(self, image, start_color, end_color):
        thickness = 0
        n_points = len(self.points) - 1
        xy_curve = [self.points[0]]
        for i, point in enumerate(self.points):
            # overlay canvas
            overlay_image = Image.new(
                "RGB",
                size=(self.image_size_px, self.image_size_px),
                color=self.image_bg_color
            )

            p1 = point
            if i == n_points:
                p2 = self.points[0]
            else:
                p2 = self.points[i+1]

            color_factor = i / n_points
            line_color = self.interpolate(start_color, end_color, color_factor)
            if i == 0:
                xy_curve.append(p2)
            else:
                xy_curve.append(p1)
                xy_curve.append(p2)
            #
            if i > int(len(self.points)/2):
                thickness -= self.scale_factor
            else:
                thickness += self.scale_factor

            if i == len(self.points):
                xy_curve = [self.points[-1], self.points[0]]

            image = self.draw_line(image, overlay_image, xy_curve, thickness, line_color)

            xy_curve = [self.points[i]]

        return image

    def generate_art(self, path: str):
        start_color = self.random_color()
        end_color = self.random_color()

        image = Image.new(
            "RGB",
            size=(self.image_size_px, self.image_size_px),
            color=self.image_bg_color
        )

        image = self.overlay_canvas(image, start_color, end_color)

        image = image.resize((self.target_size_px, self.target_size_px),
                             resample=Image.Resampling.LANCZOS)
        image.save(path)
        self.points = []


if __name__ == "__main__":
    generator = NftGenerator()

    for i in range(5):
        generator.points_generator()
        generator.center_the_image()
        generator.generate_art(f"nft_2/infinity_1_{i}.png")
