import tkinter as tk
from PIL import Image, ImageTk

class MazeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабиринт с Грейси")
        
        # Создаем холст для игры
        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()
        
        self.restart_button = None
        
        self.texture("res/gracy.png", 600, 600, 0, 0)
        # Устанавливаем фоновое изображение
        self.canvas.update()
        
        # Создаем лабиринт
        self.create_maze()
        
        # Создаем шарик-игрока
        self.piece = self.canvas.create_oval(20, 20, 40, 40, fill="white", tags="player")
        
        # Привязываем события Drag & Drop к игроку
        self.canvas.tag_bind("player", "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind("player", "<B1-Motion>", self.on_drag_motion)

    def texture(self, image_path, sx, sy, cx, cy):
        """Загружает и устанавливает фоновое изображение."""
        try:
            image = Image.open(image_path)
            image = image.resize((sx, sy), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(image)
            self.canvas.create_image(cx, cy, anchor=tk.NW, image=self.bg_image)
        except Exception as e:
            print("Ошибка загрузки изображения:", e)
    
    def create_maze(self):
        """Создает стены лабиринта и выход."""
        self.walls = [
            (75, 0, 75, 450), (150, 75, 150, 600), (225, 0, 225, 450), (300, 150, 300, 600),
            (375, 0, 375, 375), (450, 75, 450, 600), (525, 0, 525, 525), (0, 525, 450, 525)
        ]
        for wall in self.walls:
            self.canvas.create_line(wall, width=5, fill="orange")
        
        # Создаем зону выхода
        self.exit = self.canvas.create_rectangle(540, 540, 580, 580, fill="white", tags="exit")
    
    def on_drag_start(self, event):
        """Запоминает начальную позицию перемещения игрока."""
        self.last_x, self.last_y = event.x, event.y
    
    def on_drag_motion(self, event):
        """Перемещает игрока, если он не сталкивается со стенами."""
        dx, dy = event.x - self.last_x, event.y - self.last_y
        if self.will_collide(dx, dy):
            # Если произошло столкновение, показываем сообщение о поражении
            self.canvas.create_text(300, 300, text="Поражение!", font=("Arial", 24), fill="red")
            self.canvas.tag_unbind("player", "<B1-Motion>")
            self.show_restart_button()
        else:
            self.canvas.move("player", dx, dy)
            self.last_x, self.last_y = event.x, event.y
            if self.check_victory():
                # Если игрок достиг выхода, показываем сообщение о победе
                self.canvas.create_text(300, 300, text="Победа!", font=("Arial", 24), fill="red")
                self.canvas.tag_unbind("player", "<B1-Motion>")
    
    def will_collide(self, dx, dy):
        """Проверяет, столкнется ли игрок со стеной после перемещения."""
        px1, py1, px2, py2 = self.canvas.coords(self.piece)
        new_x1, new_y1, new_x2, new_y2 = px1 + dx, py1 + dy, px2 + dx, py2 + dy
        for wall in self.walls:
            wx1, wy1, wx2, wy2 = wall
            if not (new_x2 < wx1 or new_x1 > wx2 or new_y2 < wy1 or new_y1 > wy2):
                return True
        return False
    
    def check_victory(self):
        """Проверяет, достиг ли игрок выхода."""
        px1, py1, px2, py2 = self.canvas.coords(self.piece)
        ex1, ey1, ex2, ey2 = self.canvas.coords(self.exit)
        return px1 >= ex1 and py1 >= ey1
    
    def show_restart_button(self):
        """Показывает кнопку для перезапуска игры."""
        if self.restart_button is None:
            self.restart_button = tk.Button(self.root, text="Заново", command=self.restart_game)
            self.restart_button.pack()
    
    def restart_game(self):
        """Перезапускает игру, сбрасывая все элементы."""
        self.canvas.delete("all")
        self.texture("res/gracy.png", 600, 600, 0, 0)
        self.create_maze()
        self.piece = self.canvas.create_oval(20, 20, 40, 40, fill="blue", tags="player")
        self.canvas.tag_bind("player", "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind("player", "<B1-Motion>", self.on_drag_motion)
        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None
    
if __name__ == "__main__":
    root = tk.Tk()
    game = MazeGame(root)
    root.mainloop()
