import random
from time import sleep
import pygame
import sys
import os
import time

class CarRacing:
    def __init__(self):
        pygame.init()
        self.display_width = 800
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.clock = pygame.time.Clock()

        # مسیر فایل‌های تصویری
        self.base_path = getattr(sys, '_MEIPASS', '.')

        # دیگر تنظیمات بازی
        self.initialize()

    def initialize(self):
        self.crashed = False
        self.lives = 3
        self.score = 0
        self.fuel = 100
        self.shield_active = False
        self.shield_end_time = None
        self.weapon_purchased = False
        self.laser_end_time = None  # زمان پایان استفاده از لیزر
        self.lasers = []  # لیست لیزرها

        # کنترل حرکت ماشین (فاصله جابجایی ماشین به چپ و راست)
        self.car_control = 50

        # مقداردهی متغیرهای مربوط به پس‌زمینه، ماشین‌ها و اجزای دیگر
        # بارگذاری ماشین بازیکن
        self.car_colors = [
            os.path.join(self.base_path, 'img', 'car.png'),
            os.path.join(self.base_path, 'img', 'car_2.png'),
            os.path.join(self.base_path, 'img', 'car_3.png')
        ]
        self.load_car_image()

        self.car_x_coordinate = (self.display_width * 0.45)
        self.car_y_coordinate = (self.display_height * 0.8)
        self.car_width = 49
        self.car_height = 100

        # بارگذاری ماشین دشمن
        self.enemy_car_colors = [
            os.path.join(self.base_path, 'img', 'enemy_car_1.png'),
            os.path.join(self.base_path, 'img', 'enemy_car_2.png'),
            os.path.join(self.base_path, 'img', 'enemy_car_3.png')
        ]
        self.load_enemy_car_image()

        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # بارگذاری تصویر پس‌زمینه
        self.bg_colors = [
            os.path.join(self.base_path, 'img', 'back_ground.jpg'),
            os.path.join(self.base_path, 'img', 'back_ground_2.jpg')
        ]
        self.load_background_image()

        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0

        # بارگذاری پمپ سوخت
        self.pumpImg_path = os.path.join(self.base_path, 'img', 'fuel_pump.png')
        try:
            self.pumpImg = pygame.image.load(self.pumpImg_path)
        except pygame.error as e:
            print(f"Error loading fuel pump image: {e}")
            sys.exit()

        self.pump_width = 49
        self.pump_height = 50
        self.pump_x = random.randint(310, 450)
        self.pump_y = random.randint(-600, -100)

    def load_car_image(self):
        try:
            self.carImg = pygame.image.load(random.choice(self.car_colors))
        except pygame.error as e:
            print(f"Error loading player car image: {e}")
            sys.exit()

    def load_enemy_car_image(self):
        try:
            self.enemy_car = pygame.image.load(random.choice(self.enemy_car_colors))
        except pygame.error as e:
            print(f"Error loading enemy car image: {e}")
            sys.exit()

    def load_background_image(self):
        try:
            self.bgImg = pygame.image.load(random.choice(self.bg_colors))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            sys.exit()

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def run_car(self):
        while not self.crashed and self.lives > 0:
            current_time = time.time()

            # بررسی وضعیت سپر دفاعی
            if self.shield_active and current_time > self.shield_end_time:
                self.shield_active = False

            # بررسی زمان پایان استفاده از لیزر
            if self.weapon_purchased and current_time > self.laser_end_time:
                self.weapon_purchased = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:  # Move left
                        if self.car_x_coordinate - self.car_control >= 310:  # Check left boundary
                            self.car_x_coordinate -= self.car_control
                    if event.key == pygame.K_d:  # Move right
                        if self.car_x_coordinate + self.car_control <= 460:  # Check right boundary
                            self.car_x_coordinate += self.car_control
                    if event.key == pygame.K_ESCAPE:  # Open menu
                        self.show_pause_menu()
                    if event.key == pygame.K_c:  # تغییر رنگ ماشین بازیکن
                        self.load_car_image()  # تغییر تصویر ماشین بازیکن
                    if event.key == pygame.K_h:  # پر کردن جون
                        if self.lives < 5:  # اگر تعداد جون کمتر از حداکثر باشد
                            self.lives += 1
                    if event.key == pygame.K_b:  # تغییر پس‌زمینه
                        self.load_background_image()
                    if event.key == pygame.K_e:  # تغییر رنگ ماشین دشمن
                        self.load_enemy_car_image()
                    if event.key == pygame.K_l and self.weapon_purchased:  # شلیک لیزر
                        # اضافه کردن لیزر به لیست لیزرها
                        laser_x = self.car_x_coordinate + self.car_width // 2
                        laser_y = self.car_y_coordinate
                        self.lasers.append([laser_x, laser_y])

            # کم شدن سوخت
            self.fuel -= 0.05
            if self.fuel <= 0:
                self.crashed = True
                self.display_message("Out of Fuel!")

            self.gameDisplay.fill(self.black)

            # نمایش جاده، پمپ سوخت، و ماشین دشمن
            self.background_road()  # فراخوانی صحیح متد
            self.run_fuel_pump(self.pump_x, self.pump_y)
            self.pump_y += self.bg_speed
            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed
            self.car(self.car_x_coordinate, self.car_y_coordinate)

            # به روز رسانی موقعیت پمپ سوخت و دشمن
            if self.pump_y > self.display_height:
                self.pump_y = random.randint(-600, -100)
                self.pump_x = random.randint(310, 450)

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(310, 450)
                self.score += 10  # افزایش امتیاز به ازای عبور از ماشین دشمن

            # بررسی برخورد با پمپ سوخت
            if (self.pump_x < self.car_x_coordinate + self.car_width and
                self.pump_x + self.pump_width > self.car_x_coordinate and
                self.pump_y < self.car_y_coordinate + self.car_height and
                self.pump_y + self.pump_height > self.car_y_coordinate):
                self.fuel = min(100, self.fuel + 30)  # Refuel, حداکثر مقدار سوخت 100 است
                self.pump_y = random.randint(-600, -100)  # جابجایی پمپ بنزین به موقعیت جدید بعد از سوخت‌گیری

            # به‌روزرسانی و نمایش لیزرها
            self.update_lasers()

            # برخورد با ماشین دشمن
            if not self.shield_active and self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if (self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width) or \
                   (self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width):
                    self.lives -= 1
                    if self.lives > 0:
                        self.reset_enemy_position()
                    else:
                        self.crashed = True
                        self.display_message("Game Over !!!")

            # نمایش اطلاعات بازی
            self.show_score(self.score)
            self.display_fuel(self.fuel)
            self.display_lives(self.lives)

            # نمایش وضعیت سپر دفاعی
            if self.shield_active:
                self.display_shield_timer(current_time)

            # نمایش تایمر اسلحه لیزری
            if self.weapon_purchased:
                self.display_weapon_timer(current_time)

            self.count += 1

            pygame.display.update()
            self.clock.tick(60)

    def update_lasers(self):
        """به‌روزرسانی و نمایش لیزرها و بررسی برخورد آنها با ماشین دشمن"""
        for laser in self.lasers[:]:
            laser[1] -= 10  # حرکت لیزر به سمت بالا
            if laser[1] < 0:
                self.lasers.remove(laser)
            else:
                pygame.draw.rect(self.gameDisplay, self.red, (laser[0], laser[1], 5, 10))

            # بررسی برخورد لیزر با ماشین دشمن
            if (self.enemy_car_startx < laser[0] < self.enemy_car_startx + self.enemy_car_width and
                self.enemy_car_starty < laser[1] < self.enemy_car_starty + self.enemy_car_height):
                self.reset_enemy_position()
                self.lasers.remove(laser)
                self.score += 50  # اضافه کردن 50 امتیاز به ازای برخورد لیزر با ماشین دشمن

    def display_shield_timer(self, current_time):
        """نمایش تایمر سپر دفاعی در گوشه بالا سمت راست"""
        if self.shield_active:
            remaining_time = max(0, int(self.shield_end_time - current_time))
            font = pygame.font.SysFont("lucidaconsole", 20)
            shield_text = font.render(f"Shield: {remaining_time}s", True, (0, 255, 0))
            self.gameDisplay.blit(shield_text, (self.display_width - 150, 10))

    def display_weapon_timer(self, current_time):
        """نمایش تایمر اسلحه لیزری در گوشه بالا سمت چپ"""
        remaining_time = max(0, int(self.laser_end_time - current_time))
        font = pygame.font.SysFont("lucidaconsole", 20)
        weapon_text = font.render(f"Laser: {remaining_time}s", True, (255, 0, 0))
        self.gameDisplay.blit(weapon_text, (self.display_width - 300, 10))

    def show_pause_menu(self):
        """نمایش منوی توقف بازی (Pause Menu)"""
        paused = True
        while paused:
            self.gameDisplay.fill(self.black)
            font = pygame.font.SysFont("lucidaconsole", 25)
            resume_text = font.render("1. Resume", True, self.white)
            marketplace_text = font.render("2. Marketplace", True, self.white)
            exit_text = font.render("3. Exit", True, self.white)

            self.gameDisplay.blit(resume_text, (self.display_width / 2 - 100, 150))
            self.gameDisplay.blit(marketplace_text, (self.display_width / 2 - 100, 200))
            self.gameDisplay.blit(exit_text, (self.display_width / 2 - 100, 250))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    self.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # Resume the game
                        paused = False
                    if event.key == pygame.K_2:  # Marketplace
                        self.marketplace()
                        paused = False
                    if event.key == pygame.K_3:  # Exit
                        paused = False
                        self.crashed = True

    def marketplace(self):
        """نمایش منوی خرید از بازار"""
        in_market = True
        while in_market:
            self.gameDisplay.fill(self.black)
            font = pygame.font.SysFont("lucidaconsole", 25)
            buy_weapon_text = font.render("1. Buy a Weapon (cost: 200 score, lasts 10 seconds)", True, self.white)
            buy_shield_text = font.render("2. Buy a Shield (cost: 200 score, lasts 5 seconds)", True, self.white)
            exit_market_text = font.render("3. Exit Marketplace", True, self.white)

            self.gameDisplay.blit(buy_weapon_text, (self.display_width / 2 - 200, 150))
            self.gameDisplay.blit(buy_shield_text, (self.display_width / 2 - 200, 200))
            self.gameDisplay.blit(exit_market_text, (self.display_width / 2 - 200, 250))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_market = False
                    self.crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:  # خرید اسلحه
                        if self.score >= 200 and not self.weapon_purchased:
                            self.weapon_purchased = True
                            self.laser_end_time = time.time() + 10  # اسلحه برای 10 ثانیه فعال است
                            self.score -= 200
                    if event.key == pygame.K_2:  # خرید سپر
                        if self.score >= 200:
                            self.shield_active = True
                            self.shield_end_time = time.time() + 5  # سپر برای 5 ثانیه فعال است
                            self.score -= 200
                    if event.key == pygame.K_3:  # خروج از بازار
                        in_market = False

    def display_message(self, msg):
        """نمایش پیام پایان بازی"""
        font = pygame.font.SysFont("comicsansms", 72, True)
        text = font.render(msg, True, self.white)
        self.gameDisplay.blit(text, (self.display_width / 2 - text.get_width() // 2, self.display_height / 2 - text.get_height() // 2))
        pygame.display.update()
        sleep(2)

    def background_road(self):
        """نمایش تصویر پس‌زمینه"""
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def run_fuel_pump(self, x, y):
        self.gameDisplay.blit(self.pumpImg, (x, y))

    def show_score(self, score):
        """نمایش امتیاز در گوشه بالا سمت چپ"""
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Score : " + str(score), True, self.white)
        self.gameDisplay.blit(text, (0, 0))

    def display_fuel(self, fuel):
        font = pygame.font.SysFont("lucidaconsole", 20)
        text = font.render("Fuel : " + str(int(fuel)), True, (255, 255, 0))
        self.gameDisplay.blit(text, (10, 40))

    def display_lives(self, lives):
        font = pygame.font.SysFont("lucidaconsole", 25)
        text = "♥ " * lives
        rendered_text = font.render(text, True, (255, 0, 0))
        self.gameDisplay.blit(rendered_text, (10, 10))

    def reset_enemy_position(self):
        self.enemy_car_starty = -600
        self.enemy_car_startx = random.randrange(310, 450)

if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()
