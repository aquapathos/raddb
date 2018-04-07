#  クォータ画像とサムネイルの作成
'''
   「2017ダイコン写真」フォルダ中の　全 jpg 画像のクォータ画像（4分の１サイズ）とサムネイル画像を生成

   クォータ画像  ->  qpic フォルダ
   サムネイル画像 -> thumb フォルダ

　　に保存するとともに、「2017ダイコンデータ.xlsx」という名のエクセルファイルを作成
'''

import os
import glob
import pandas as pd
import numpy as np
from PIL import Image
import re # 正規表現処理ライブラリ

from terminology import labelDic as labelDic

# デフォルトの処理対象画像の正規表現
pathpattern = '2017ダイコン写真/*.jpg'

# デフォルトのクォータ画像の保存先
quarter_dir = './qpics/'

# デフォルトのサムネイル画像の保存先
thumbnail_dir = './thumb/'

# デフォルトのサムネイルのサイズ
thumbnail_size = (128,128)

# デフォルトのエクセルファイル名
excelfile = '2017ダイコンデータ.xlsx'

# デフォルトのシート名
sheetname = '2017ダイコンデータ'

# クォータ画像とサムネイル画像の生成
def makeQuarter(pathpattern=pathpattern,qdir = quarter_dir, tdir = thumbnail_dir, withthumb = True, overwrite = False):
    files = glob.glob(pathpattern)
    if not os.path.exists(qdir):
        os.makedirs(qdir)
    if withthumb and not os.path.exists(tdir):
        os.makedirs(tdir)

    for f in files:  
        fname = os.path.basename(f)
        
        needopen = True
        if overwrite or not os.path.exists(qdir+fname):
            img = Image.open(f)
            img_resize = img.resize((int(img.width/4), int(img.height/4)))
            img_resize.save(qdir + fname)
            needopen = False
            
        if overwrite or not os.path.exists(tdir+fname):
            if needopen:
                img = Image.open(f)
            thumbnail_size = (128,128)
            img.thumbnail(thumbnail_size) # 破壊的メソッドであるので注意
            img.save(tdir+fname)

# 表データの生成
def makeTable(pathpattern=pathpattern,needExcel = False, tofile=excelfile,sheet_name=sheetname):
    # ecolumns =['filename', 'year','spacies', 'block', 'shape','sn']
    dCol = ['ファイル名', '年','品種', '区画', '形状','シリアルNo.']
    df = pd.DataFrame(columns = dCol)
    files = glob.glob(pathpattern)  
    for f in files:    
        fname = os.path.basename(f)
        try:  # \d +数字列　あるいは \D 数字以外の列   を取り出す　（　| は縦棒であることに注意） 
            (year,spacies, block, shape,sn,_) = re.findall(r'(\d+|\D+)',fname)
            sn = ('00'+sn)[-3:]
            block = ('0'+block)[-2:]
            spacies = labelDic[spacies]
        except:
            continue
        sd = pd.Series({dCol[0]:fname, dCol[1]:year, dCol[2]:spacies, dCol[3]:block, dCol[4]:shape,dCol[5]:sn })
        df = df.append(sd, ignore_index=True)
    df = df.sort_values(by=[dCol[2],dCol[3],dCol[4],dCol[5]])
    df.to_excel(tofile,sheet_name=sheet_name)
    return df

def main():
    makeQuarter()
    makeTable(needExcel=True)

if __name__ == '__main__':
    main()