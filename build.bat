mkdir dist\meta
mkdir dist\docs
copy meta dist\meta
copy docs dist\docs
pyinstaller src/main.py -F --name=doclens --distpath=dist/bin/ --specpath=dist/bin/ --workpath=build