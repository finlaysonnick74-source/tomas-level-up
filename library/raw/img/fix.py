from PIL import Image, ImageDraw, ImageFont
F="/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
def badge(d,x,y,w,h,text,fs):
    d.rounded_rectangle([x,y,x+w,y+h],radius=6,fill=(160,160,160),outline=(120,120,120),width=2)
    f=ImageFont.truetype(F,fs); tw=d.textlength(text,font=f)
    d.text((x+(w-tw)/2,y+(h-fs)/2-2),text,font=f,fill="white")
s=1264/1024
im=Image.open("d05.jpg").convert("RGB"); d=ImageDraw.Draw(im)
d.rectangle([int(812*s),int(32*s),1264,int(199*s)],fill="white")
im.save("d05.jpg",quality=92)
for n in ["d05"]:
    im=Image.open(n+".jpg").convert("RGB"); d=ImageDraw.Draw(im)
    # corner tag
    f=ImageFont.truetype(F,26)
    t="BACK VIEW  ·  front: original brand logo untouched"
    tw=d.textlength(t,font=f)
    d.rounded_rectangle([1264-tw-60,1264-70,1264-20,1264-22],radius=10,fill=(150,150,150))
    d.text((1264-tw-40,1264-64),t,font=f,fill="white")
    im.save(n+".jpg",quality=92)
im=Image.open("d08.jpg").convert("RGB"); d=ImageDraw.Draw(im)
badge(d,int(655*s),int(200*s),int(115*s),int(28*s),"original brand logo",17)
im.save("d08.jpg",quality=92)
