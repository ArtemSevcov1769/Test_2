#IMPORT
from PyQt5.QtWidgets import (QLabel, QWidget, QListWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QApplication, QFileDialog, QInputDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
import os
#IMPORT

app = QApplication([])
window = QWidget()

#BTN
btn_dir = QPushButton('Открыть папку')
btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_mirror = QPushButton('Зеркало по |')
btn_mirror2 = QPushButton('Зеркало по ——')
btn_sharp = QPushButton('Резкость')
btn_blur = QPushButton('Блюр')
btn_countr = QPushButton('Контур')
btn_embos = QPushButton('Объём')
btn_bw = QPushButton('Ч/Б')
#BTN

#BOX
h_main = QHBoxLayout()
h_btn = QHBoxLayout()
v_left = QVBoxLayout()
v_right = QVBoxLayout()
#BOX

#CONNECTION
image_list = QListWidget()
image = QLabel('')
h_btn.addWidget(btn_left)
h_btn.addWidget(btn_right)
h_btn.addWidget(btn_mirror)
h_btn.addWidget(btn_mirror2)
h_btn.addWidget(btn_sharp)
h_btn.addWidget(btn_blur)
h_btn.addWidget(btn_bw)
h_btn.addWidget(btn_embos)
v_left.addWidget(btn_dir)
v_left.addWidget(image_list)
h_btn.addWidget(btn_countr)
v_right.addWidget(image)
v_right.addLayout(h_btn)
h_main.addLayout(v_left, stretch=2)
h_main.addLayout(v_right, stretch=6)
#CONNECTION

#WINDOW AND SIZE
window.resize(1080, 720)
window.setWindowTitle('EasyEditor')
window.setLayout(h_main)
#WINDOW AND SIZE

#GET-DIR
curDir = ''
def get_dir():
    path = QFileDialog.getExistingDirectory()
    return path
#GET_DIR

#SHOW_FILES
def show_files():
    path = get_dir()
    if len(path) >= 0:
        global curDir
        curDir = path
        files = os.listdir(path)
        extension = ['.png', '.jpg', '.jpeg', '.svg', '.eps', '.bmp']
        images = filter(files, extension)
        image_list.clear()
        image_list.addItems(images)
#SHOW_FILES

#FILTER
def filter(files, extension):
    images = []
    for file in files:
        for ext in extension:
            if file.endswith(ext):
                images.append(file)
    return images
#FILTER

#IMAGE_PROCESSOR
class ImageProcessor:
    def __init__(self):
        self.dir = None
        self.filename = None
        self.image = None
        self.save_dir = 'Modifed'

    #загрузка_изображения
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        img_path = os.path.join(dir, filename)
        self.image = Image.open(img_path)

    #показ
    def showImage(self, path):
        image.hide()
        pixmap = QPixmap(path)
        w, h = image.width(), image.height()
        pixmap = pixmap.scaled(w, h, Qt.KeepAspectRatio)
        image.setPixmap(pixmap)
        image.show()

    #сохранение в папку 'Modifed'
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.isdir(path) or os.path.exists(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    #сокращение сохранения для def
    def saves(self):
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.filename)
        self.showImage(image_path)

    #Ч/Б
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saves()

    #зеркало по верт
    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saves()

    #зеркало по гориз
    def mirror_2(self):
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        self.saves()

    #поворот направо
    def rotate_r(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saves()

    #повернуть налево
    def rotate_l(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saves()

    #резкость
    def sharpn(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saves()

    #блюр
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saves()

    #объём
    def embos(self):
        self.image = self.image.filter(ImageFilter.EMBOSS)
        self.saves()

    #контур
    def countr(self):
        self.image = self.image.filter(ImageFilter.CONTOUR)
        self.saves()

imgProc = ImageProcessor()
#IMAGE_PROCESSOR

#SHOW_CURRENT_IMAGE
def showCurrentImage():
    if image_list.currentRow() >= 0:
        filename = image_list.currentItem().text()
        imgProc.loadImage(curDir, filename)
        img_path = os.path.join(curDir, filename)
        imgProc.showImage(img_path)
#SHOW_CURRENT_IMAGE

#CLICKED_CONNECT
btn_bw.clicked.connect(imgProc.do_bw)
btn_dir.clicked.connect(show_files)
btn_mirror.clicked.connect(imgProc.mirror)
btn_right.clicked.connect(imgProc.rotate_r)
image_list.currentRowChanged.connect(showCurrentImage)
btn_left.clicked.connect(imgProc.rotate_l)
btn_sharp.clicked.connect(imgProc.sharpn)
btn_blur.clicked.connect(imgProc.blur)
btn_embos.clicked.connect(imgProc.embos)
btn_countr.clicked.connect(imgProc.countr)
btn_mirror2.clicked.connect(imgProc.mirror_2)
#CLICKED_CONNECT

#SHOW
window.show()
app.exec()
#SHOW