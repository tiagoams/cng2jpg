# cng2jpg
Convert "Complete National Geographic" CNG files to JPG using python

## Requirements

Python 3 with `pillow` package. This package can be installed using conda:

```
conda install pillow
```

## Basic usage

### copying from CD into local hard drive:

```sh
python cng2jpg.py --src /run/media/_user_/CNG_DISC1/disc1/images --dst ~/CNG/discs/images
```

### convert a hard drive copy

```sh
python cng2jpg.py --src ~/CNG/discs  --dst ~/CNG/discs/images [--remove] [--merge]
```

or in Windows

```
python cng2jpg.py --src C:\users\myuser\CNG\discs  --dst C:\users\myuser\CNG\discs\images [--remove] [--merge]
```

Use --remove to get rid of .cng files as they are converted, to avoid needing extra 40+GB of space for both jpg and cng.

Use --merge to merge double spread pages into single files. Due to erros in the original scans the pages don't align perfectly.

## References

"The cng files are all jpegs, XOR'd bitwise with 239"

http://www.subdude-site.com/WebPages_Local/RefInfo/Computer/Linux/LinuxGuidesByBlaze/appsImagePhotoTools/cng2jpgGuide/cng2jpg_guide.htm
