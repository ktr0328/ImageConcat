# ImageConcat

画像群をPDFに結合する。

## Usage

```sh
Usage: index.py [OPTIONS] IMG_DIR

Options:
  --save_dir TEXT
  --ulid BOOLEAN
  --quality INTEGER
  --help             Show this message and exit.

python3 src/index.py {target dir} --ulid false
```

### Params

#### IMG_DIR

イメージファイルのディレクトリ。

```sh
example
|-- 1
    |-- 1.jpg
    |-- 2.png
    |-- ...
|-- 2
`-- 3
```

#### save_dir

出力先。
デフォルトは./output/pdf/{ulid}

#### ulid

出力されるPDFファイル名をULIDにするか。
falseならディレクトリ名が使用される。

#### quality

PDFに結合する際、pngの透過が消え、RGBに変換される。
元ファイルが書き変わる(png -> jpeg)ため、バックアップを推奨。
その際の画質。
1 ~ 100(int)

## Log

`logs/common/{YYYY-MM}/{DD}.log`
