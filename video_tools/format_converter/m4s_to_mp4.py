import os
dizhi = "video"
files = os.listdir(dizhi)
def file_filter(f):
    if f[-4:]=='.m4s':
        return True
    else:
        return False
    
files = list(filter(file_filter,files))
weizhi=[]
for i in range(len(files)):
    weizhi.append(dizhi+'\\'+files[i])

for i in range (len(files)):
    files[i]=files[i][:-3]+'mp4'
xinweizhi=[]
for i in range(len(files)):
    xinweizhi.append(dizhi+'\\'+files[i])
    
def fix_m4s(target_path: str, output_path: str, bufsize: int = 256*1024*1024) -> None:
    assert bufsize > 0
    with open(target_path, 'rb') as target_file:
        header= target_file.read(32)
        new_header = header.replace(b'000000000',b'')
        new_header = new_header.replace(b's',b'')
        new_header =new_header.replace(b'avci', b'')
        with open(output_path, 'wb') as output_file:
            output_file.write(new_header)
            i=target_file.read(bufsize)
            while i:
                output_file.write(i)
                i=target_file.read(bufsize)
for i in range(len(files)):
    fix_m4s(weizhi[i],xinweizhi[i])