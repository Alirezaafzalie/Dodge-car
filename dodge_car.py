import random
from time import sleep
import pygame
import sys
import os
import time
import tkinter as tk
from tkinter import messagebox
import pickle

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
        self.font = pygame.font.Font(None, 36)  # فونت پیش‌فرض با اندازه 36

        # Set working directory to script location
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
        self.car_colors = [
            os.path.join(self.base_path, 'img', 'car.png'),
            os.path.join(self.base_path, 'img', 'car_2.png'),
            os.path.join(self.base_path, 'img', 'car_3.png')
        ]
        self.car_selected = 0  # ماشین پیش‌فرض (car.png)
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
            sys.exit("Required image files are missing. Please check the 'img' folder.")

        self.pump_width = 49
        self.pump_height = 50
        self.pump_x = random.randint(310, 450)
        self.pump_y = random.randint(-600, -100)


    def save_game(self):
        save_path = os.path.join(os.path.dirname(__file__), "savegame.pkl")  # تورفتگی 4 فاصله
        save_data = {
            'lives': self.lives,
            'score': self.score,
            'fuel': self.fuel,
            'car_x_coordinate': self.car_x_coordinate,
            'car_y_coordinate': self.car_y_coordinate,
            'enemy_car_startx': self.enemy_car_startx,
            'enemy_car_starty': self.enemy_car_starty,
            'enemy_car_speed': self.enemy_car_speed,
            'bg_y1': self.bg_y1,
            'bg_y2': self.bg_y2
        }
        try:
            with open(save_path, "wb") as f:
                pickle.dump(save_data, f)
            print("Game Saved!")
        except Exception as e:
            print(f"Error saving game: {e}")
    def load_game(self):
        save_path = os.path.join(os.path.dirname(__file__), "savegame.pkl")
        try:
            with open(save_path, "rb") as f:
                save_data = pickle.load(f)
                self.lives = save_data['lives']
                self.score = save_data['score']
                self.fuel = save_data['fuel']
                self.car_x_coordinate = save_data['car_x_coordinate']
                self.car_y_coordinate = save_data['car_y_coordinate']
                self.enemy_car_startx = save_data['enemy_car_startx']
                self.enemy_car_starty = save_data['enemy_car_starty']
                self.enemy_car_speed = save_data['enemy_car_speed']
                self.bg_y1 = save_data['bg_y1']
                self.bg_y2 = save_data['bg_y2']
            print("Game Loaded!")
        except FileNotFoundError:
            print("No saved game found. Starting a new game.")
        except Exception as e:
            print(f"Error loading game: {e}")



    def load_car_image(self):
        try:
            self.carImg = pygame.image.load(self.car_colors[self.car_selected])
        except pygame.error as e:
            print(f"Error loading player car image: {e}")
            sys.exit("Required car image files are missing. Please check the 'img' folder.")

    def load_enemy_car_image(self):
        try:
            selected_enemy_car = random.choice(self.enemy_car_colors)
            self.enemy_car = pygame.image.load(selected_enemy_car)
        except pygame.error as e:
            print(f"Error loading enemy car image: {e}")
            sys.exit("Required enemy car image files are missing. Please check the 'img' folder.")

    def load_background_image(self):
        try:
            selected_bg = random.choice(self.bg_colors)
            self.bgImg = pygame.image.load(selected_bg)
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            sys.exit("Background image file is missing. Please check the 'img' folder.")

    def car(self, car_x_coordinate, car_y_coordinate):
        self.gameDisplay.blit(self.carImg, (car_x_coordinate, car_y_coordinate))

    def display_lives(self):
    # ساخت متن با کاراکتر قلب
        heart_text = self.font.render(f"Lives: {'\u2764 ' * self.lives}", True, self.red)
    # رسم متن در بالای صفحه
        self.gameDisplay.blit(heart_text, (10, 10))

    def display_fuel(self):
        pygame.draw.rect(self.gameDisplay, self.green, (10, 50, self.fuel, 20))
        pygame.draw.rect(self.gameDisplay, self.white, (10, 50, 100, 20), 2)
    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.white)  # متن امتیاز
        self.gameDisplay.blit(score_text, (10, 80))  # رسم متن روی صفحه در موقعیت مشخص
    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.show_main_menu()

    def run_car(self):
        self.crashed = False
        while not self.crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.car_x_coordinate -= self.car_control
                    if event.key == pygame.K_d:
                        self.car_x_coordinate += self.car_control
                    if event.key == pygame.K_b:
                        self.load_background_image()
                    if event.key == pygame.K_ESCAPE:
                        self.show_main_menu()
                    if event.key == pygame.K_h:
                        if self.lives < 5:  # Maximum 5 lives allowed
                            self.lives += 1
                    if event.key == pygame.K_f:
                        if self.fuel < 100:
                            self.fuel += 25
                    if event.key == pygame.K_s:
                        self.score += 50
                    if event.key == pygame.K_c:
                        self.bg_speed -= 5
                        self.enemy_car_speed -= 100
                    if event.key == pygame.K_SPACE:  # شلیک با دکمه Space
                        self.fire_weapon()

            # Increase speed based on score
            self.enemy_car_speed = 5 + (self.score // 50)
            self.bg_speed = 3 + (self.score // 100)

            # Check if car is out of bounds
            if self.car_x_coordinate < 310 or self.car_x_coordinate > 460:
                self.lives -= 1
                if self.lives == 0:
                    self.crashed = True

            # Draw background
            self.gameDisplay.fill(self.black)
            self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1))
            self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y2))

            # Move background
            self.bg_y1 += self.bg_speed
            self.bg_y2 += self.bg_speed

            if self.bg_y1 >= self.display_height:
                self.bg_y1 = -self.display_height
            if self.bg_y2 >= self.display_height:
                self.bg_y2 = -self.display_height

            # Draw car
            self.car(self.car_x_coordinate, self.car_y_coordinate)

            # Draw enemy car
            self.gameDisplay.blit(self.enemy_car, (self.enemy_car_startx, self.enemy_car_starty))
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = -self.enemy_car_height
                self.enemy_car_startx = random.randint(310, 450)
                self.score += 10

            # Check collision
            if self.car_y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car_x_coordinate > self.enemy_car_startx and self.car_x_coordinate < self.enemy_car_startx + self.enemy_car_width or \
                        self.car_x_coordinate + self.car_width > self.enemy_car_startx and self.car_x_coordinate + self.car_width < self.enemy_car_startx + self.enemy_car_width:
                    self.lives -= 1
                    self.enemy_car_starty = -self.enemy_car_height
                    if self.lives == 0:
                        self.crashed = True

            # Fuel pump logic
            self.gameDisplay.blit(self.pumpImg, (self.pump_x, self.pump_y))
            self.pump_y += self.bg_speed
            if self.pump_y > self.display_height:
                self.pump_y = random.randint(-600, -100)
                self.pump_x = random.randint(310, 450)

            # Check fuel collection
            if self.pump_x < self.car_x_coordinate + self.car_width and self.pump_x + self.pump_width > self.car_x_coordinate:
                if self.pump_y < self.car_y_coordinate + self.car_height and self.pump_y + self.pump_height > self.car_y_coordinate:
                    self.fuel = min(100, self.fuel + 30)
                    self.pump_y = random.randint(-600, -100)

            # Decrease fuel
            self.fuel -= 0.1
            if self.fuel <= 0:
                self.crashed = True

            # Display lives and fuel
            self.display_lives()
            self.display_fuel()
            self.display_score()

            pygame.display.update()
            self.clock.tick(60)

    def show_main_menu(self):
        root = tk.Tk()
        root.title("Main Menu")
        root.configure(bg="black")

        def start_game():
            print("Start Game button clicked!")
            root.destroy()
            self.run_car()

        def open_marketplace():
            root.destroy()
            self.show_marketplace()

        def exit_game():
            root.destroy()
            self.crashed = True

        tk.Label(root, text="Car Racing Game", font=("Helvetica", 20), fg="white", bg="black").pack(pady=20)
        tk.Button(root, text="Start Game", font=("Helvetica", 16), command=start_game, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Marketplace", font=("Helvetica", 16), command=open_marketplace, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Exit", font=("Helvetica", 16), command=exit_game, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Save Game", font=("Helvetica", 16), command=self.save_game, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Load Game", font=("Helvetica", 16), command=self.load_game, bg="gray", fg="white").pack(pady=10)

        root.mainloop()

    def show_marketplace(self):
        root = tk.Tk()
        root.title("Marketplace")
        root.configure(bg="black")

        def buy_weapon():
            if self.score >= 200 and not self.weapon_purchased:
                self.weapon_purchased = True
                self.laser_end_time = time.time() + 10
                self.score -= 200
                messagebox.showinfo("Purchase", "Weapon purchased!")
            else:
                messagebox.showerror("Error", "Not enough score or weapon already purchased!")

        def buy_shield():
            if self.score >= 200:
                self.shield_active = True
                self.shield_end_time = time.time() + 5
                self.score -= 200
                messagebox.showinfo("Purchase", "Shield purchased!")
            else:
                messagebox.showerror("Error", "Not enough score!")

        def buy_car_3():
            if self.score >= 200:
                self.car_selected = 2
                self.load_car_image()
                self.score -= 200
                messagebox.showinfo("Purchase", "Car 3 purchased!")
            else:
                messagebox.showerror("Error", "Not enough score!")

        def buy_car_2():
            if self.score >= 300:
                self.car_selected = 1
                self.load_car_image()
                self.score -= 300
                messagebox.showinfo("Purchase", "Car 2 purchased!")
            else:
                messagebox.showerror("Error", "Not enough score!")

        def exit_market():
            root.destroy()
            self.show_main_menu()

        tk.Label(root, text="Marketplace", font=("Helvetica", 20), fg="white", bg="black").pack(pady=20)
        tk.Button(root, text="Buy Weapon (200 score)", font=("Helvetica", 16), command=buy_weapon, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Buy Shield (200 score)", font=("Helvetica", 16), command=buy_shield, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Buy Car 3 (200 score)", font=("Helvetica", 16), command=buy_car_3, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Buy Car 2 (300 score)", font=("Helvetica", 16), command=buy_car_2, bg="gray", fg="white").pack(pady=10)
        tk.Button(root, text="Exit Marketplace", font=("Helvetica", 16), command=exit_market, bg="gray", fg="white").pack(pady=10)

        root.mainloop()

if __name__ == '__main__':
    car_racing = CarRacing()
    car_racing.racing_window()