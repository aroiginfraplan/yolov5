import sys
import getopt
import os
import shutil
import numpy as np
from sklearn.model_selection import train_test_split


def get_inputfolder(argv):
    inputfolder = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        missing_inputfolder()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            missing_inputfolder()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfolder = arg
    
    if not inputfolder:
        missing_inputfolder()
        return

    print('Splitting database:', inputfolder)
    return inputfolder


def get_files_path(inputfolder):
    PATH = inputfolder + '/obj_train_data'
    list_img = []
    list_txt = []
    for folder in os.listdir(PATH):
        path_folder = PATH + '/' + folder
        for file in os.listdir(path_folder):
            if file.endswith('.txt'):
                list_txt.append(path_folder + '/' + file)
            else:
                list_img.append(path_folder + '/' + file)
    list_img.sort()
    list_txt.sort()
    return list_img, list_txt


def mv_img_txt(inputfolder, src_img, src_txt, _type):
    pwd = os.getcwd() + '/'
    f = open(inputfolder + '/' + _type + '.txt', 'w')
    
    for i in range(len(src_img)):
        dest_img = src_img[i].replace('/obj_train_data', '/images/' + _type)
        dest_img_folder = '/'.join(dest_img.split('/')[:-1])
        if not os.path.exists(dest_img_folder):
            os.makedirs(dest_img_folder)
        os.replace(src_img[i], dest_img)
        f.write(dest_img + '\n')

        dest_txt = src_txt[i].replace('/obj_train_data', '/labels/' + _type)
        dest_txt_folder = '/'.join(dest_txt.split('/')[:-1])
        if not os.path.exists(dest_txt_folder):
            os.makedirs(dest_txt_folder)
        os.replace(src_txt[i], dest_txt)
    
    f.close()

def mv_train_test_val(
    inputfolder, img_train, txt_train, img_test, txt_test, img_val, txt_val
):
    mv_img_txt(inputfolder, img_train, txt_train, 'train')
    mv_img_txt(inputfolder, img_test, txt_test, 'test')
    mv_img_txt(inputfolder, img_val, txt_val, 'val')
    shutil.rmtree(inputfolder + '/obj_train_data')

def missing_inputfolder():
    print('missing <inputfolder>:')
    print('split_dataset.py -i <inputfolder>')


def main(argv):
    inputfolder = get_inputfolder(argv)

    img_list, txt_list = get_files_path(inputfolder)

    img_train, img_test, txt_train, txt_test = train_test_split(img_list, txt_list, test_size=0.4, random_state=1)
    img_test, img_val, txt_test, txt_val = train_test_split(img_test, txt_test, test_size=0.5, random_state=1)
    mv_train_test_val(inputfolder, img_train, txt_train, img_test, txt_test, img_val, txt_val)

if __name__ == '__main__':
    main(sys.argv[1:])
