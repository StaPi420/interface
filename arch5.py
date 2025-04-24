import struct
import array
from itertools import chain

def f_int(num):
    try:
        with open('file.bin',  'wb') as f:
            f.write(struct.pack('h', num))

        with open('file.bin', 'rb') as f:
            print(f"Преобразование для числа {num}: {struct.unpack('H', f.read())[0]}")
    except struct.error:
        print('Произошла ошибка')

f_int(11)

f_int(32767)

f_int(-32767)

f_int(-15000)

f_int(50000)


def f_float(num):
    try:
        with open('file.bin',  'wb') as f:
            f.write(struct.pack('f', num))

        with open('file.bin', 'rb') as f:
            print(f"Преобразование для числа {num}: {struct.unpack('i', f.read())}")
    except struct.error:
        print('Произошла ошибка')

f_float(52523.0)

f_float(3.4e+38)

f_float(3.4e-38)

f_float(4e+380)


with open('file.bin', 'wb') as f:
    f.write(struct.pack('>hh', -32641, 0))

with open('file.bin', 'rb') as f:
    print(f'Задуманное вещественное число: {struct.unpack('>f', f.read())[0]}')

with open('in.bmp', 'rb') as inp, open('out_negativ.bmp', 'wb') as out:
    head = inp.read(54)
    a = array.array('B', inp.read())
    for i in range(0, len(a), 3):
        a[i] = 255 - a[i]
        a[i + 1] = 255 - a[i + 1]
        a[i + 2] = 255 - a[i + 2]
    out.write(head)
    out.write(a.tobytes())

with open('in.bmp', 'rb') as inp, open('out_bright.bmp', 'wb') as out:
    head = inp.read(54)
    a = array.array('B', inp.read())
    for i in range(len(a)):
        if a[i] > 55:
            a[i] = 255
        else:
            a[i] += 150
    out.write(head)
    out.write(a.tobytes())
        
with open('in.bmp', 'rb') as inp, open('out_dark.bmp', 'wb') as out:
    head = inp.read(54)
    a = array.array('B', inp.read())
    for i in range(len(a)):
        if a[i] < 100:
            a[i] = 0
        else:
            a[i] -= 100
    out.write(head)
    out.write(a.tobytes())



with open('in.bmp', 'rb') as inp, open('out_mirrored1.bmp', 'wb') as out:
    head = inp.read(18)
    width = struct.unpack('i', inp.read(4))[0]
    height = struct.unpack('i', inp.read(4))[0]
    other = inp.read(28)
    a_mat = array.array('B', inp.read())
    row_size = width * 3
    for y in range(height // 2):
        top_row_start = y * row_size
        top_row_end = top_row_start + row_size
        bottom_row_start = (height - y - 1) * row_size
        bottom_row_end = bottom_row_start + row_size

        top_row = a_mat[top_row_start:top_row_end]
        bottom_row = a_mat[bottom_row_start:bottom_row_end]
        a_mat[top_row_start:top_row_end] = bottom_row
        a_mat[bottom_row_start:bottom_row_end] = top_row


    out.write(head)
    out.write(struct.pack('i', width))
    out.write(struct.pack('i', height))
    out.write(other)
    out.write(array.array('B', a_mat).tobytes())

with open('in.bmp', 'rb') as inp, open('out_mirrored2.bmp', 'wb') as out:
    head = inp.read(18)
    width = struct.unpack('i', inp.read(4))[0]
    height = struct.unpack('i', inp.read(4))[0]
    other = inp.read(28)
    a = array.array('B', inp.read())   
    row_size = width*3
    for i in range(height):
        row_start = i * row_size
        row_end = row_start + row_size
        for j in range(0, row_size // 2, 3):
            b = a[row_start + j]
            g = a[row_start + j + 1]
            r = a[row_start + j + 2]
            a[row_start + j] = a[row_end - 3 - j]
            a[row_start + j + 1] = a[row_end - 2 - j]
            a[row_start + j + 2] = a[row_end - 1 - j]
            a[row_end - 3 - j] = b
            a[row_end - 2 - j] = g
            a[row_end - 1 - j] = r
    out.write(head)
    out.write(struct.pack('i', width))
    out.write(struct.pack('i', height))
    out.write(other)
    out.write(a.tobytes())

with open('in.bmp', 'rb') as inp, open('out_grayscale.bmp', 'wb') as out:
    head = inp.read(54)
    a = array.array('B', inp.read())
    for i in range(0, len(a), 3):
        gray = int(0.3 * a[i + 2] + 0.6 * a[i + 1] + 0.1 * a[i])
        a[i] = gray       
        a[i + 1] = gray   
        a[i + 2] = gray   
    out.write(head)
    out.write(a.tobytes())

with open('in.bmp', 'rb') as inp, open('out_rotated_90.bmp', 'wb') as out:
    head = inp.read(18)
    width = struct.unpack('i', inp.read(4))[0]
    height = struct.unpack('i', inp.read(4))[0]
    other = inp.read(28)
    a = array.array('B', inp.read())

    row_size = width * 3
    rotated = array.array('B', [0] * len(a))
    for y in range(height):
        for x in range(width):
            src_index = (y * row_size) + (x * 3)
            dest_index = ((x * height) + (height - y - 1)) * 3

            rotated[dest_index] = a[src_index]       
            rotated[dest_index + 1] = a[src_index + 1]  
            rotated[dest_index + 2] = a[src_index + 2]  

    out.write(head)
    out.write(struct.pack('i', height)) 
    out.write(struct.pack('i', width))  
    out.write(other)
    out.write(rotated.tobytes())