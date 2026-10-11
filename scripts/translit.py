# Transliterasi Arab berharakat -> Latin (skema Indonesia, selaras dengan words.json)
import re
FATHA,DAMMA,KASRA,SUKUN,SHADDA='\u064E','\u064F','\u0650','\u0652','\u0651'
TAN={'\u064B':'an','\u064C':'un','\u064D':'in'}
DAGGER='\u0670'
MARKS=set([FATHA,DAMMA,KASRA,SUKUN,SHADDA,DAGGER]+list(TAN))
C={'ب':'b','ت':'t','ث':'ṡ','ج':'j','ح':'ḥ','خ':'kh','د':'d','ذ':'ż','ر':'r','ز':'z','س':'s','ش':'sy','ص':'ṣ','ض':'ḍ','ط':'ṭ','ظ':'ẓ','ع':'‘','غ':'gh','ف':'f','ق':'q','ك':'k','ل':'l','م':'m','ن':'n','ه':'h','ء':'’','ؤ':'’','ئ':'’','أ':'’','إ':'’','آ':'’ā','پ':'p','چ':'c','ڤ':'v','گ':'g'}
SUN=set('تثدذرزسشصضطظلن')
VOW={FATHA:'a',DAMMA:'u',KASRA:'i'}
PUNCT={'؟':'?','،':',','؛':';'}

def split_units(word):
    """pecah kata menjadi [(huruf, set_tanda)]"""
    units=[]
    for ch in word:
        if ch in MARKS:
            if units: units[-1][1].add(ch)
        elif ch=='\u0640': continue
        else: units.append([ch,set()])
    return units

def tr_word(word, first_in_phrase=True):
    u=split_units(word)
    out=[];i=0;n=len(u);after_art=-1
    def vowel_of(marks):
        for m in marks:
            if m in VOW: return VOW[m]
        for m in marks:
            if m in TAN: return TAN[m]
        return None
    while i<n:
        ch,mk=u[i]
        # artikel al-
        if ch in 'اٱ' and i!=after_art and not mk and i+1<n and u[i+1][0]=='ل' and (SUKUN in u[i+1][1] or (not u[i+1][1] and i+2<n and SHADDA in u[i+2][1])):
            prev_vowel_alif = i>0 and FATHA in u[i-1][1]
            if not prev_vowel_alif or i==0 or u[i-1][0] in 'وفبكل':
                nxt=u[i+2][0] if i+2<n else ''
                x=C.get(nxt,'l') if nxt in SUN else 'l'
                lead = out and any(c in 'aiu' for c in ''.join(out)[-1:])
                out.append(('' if (out and not first_in_phrase) or out else 'a')+x+'-' if True else '')
                i+=2; after_art=i
                if nxt in SUN:
                    # huruf matahari: jangan dobel karena sudah ada pada x-; lewati shadda saat mencetak huruf berikutnya
                    u[i][1].discard(SHADDA)
                continue
        # ال + kata berawalan alif wasal: lam berharakat kasra (الِاسْتِخْدَامِ)
        if ch in 'اٱ' and not mk and i+2<n and u[i+1][0]=='ل' and KASRA in u[i+1][1] and u[i+2][0] in 'اٱ' and not any(m in u[i+2][1] for m in VOW):
            out.append(('' if out else 'a')+'l-'); i+=2; after_art=i; continue
        # alif hamzah wasal / awal kata
        if ch in 'اٱ':
            v=vowel_of(mk)
            if i==0 or i==after_art:
                out.append(v or 'i'); i+=1; continue
            # alif panjang
            if i>0 and FATHA in u[i-1][1] and not mk: out.append('ā'); i+=1; continue
            if any(m in TAN for m in u[i-1][1]) : i+=1; continue
            out.append(v or ''); i+=1; continue
        if ch=='ى':
            out.append('ā' if i>0 and FATHA in u[i-1][1] else 'ī'); i+=1; continue
        if ch=='ة':
            v=vowel_of(mk)
            if v: out.append('t'+v)
            else: out.append('h')
            i+=1; continue
        if ch in 'وي':
            base='w' if ch=='و' else 'y'
            long_ch='ū' if ch=='و' else 'ī'
            pv = None
            if i>0:
                pv = vowel_of(u[i-1][1]) if not any(m in TAN for m in u[i-1][1]) else None
            v=vowel_of(mk)
            if SHADDA in mk:
                s=base*2
                if v=='a' and i+1<n and not u[i+1][1] and u[i+1][0] in 'اى': out.append(s+'ā'); i+=2; continue
                out.append(s+(v or '')); i+=1; continue
            if not mk and i>0 and ((ch=='و' and pv=='u') or (ch=='ي' and pv=='i')):
                out.append(long_ch); i+=1; continue
            if SUKUN in mk and i>0 and pv=='a':
                out.append(base); i+=1; continue
            chunk=base
            if v=='i' and i+1<n and not u[i+1][1] and u[i+1][0]=='ي': out.append(chunk+'ī'); i+=2; continue
            if v=='u' and i+1<n and not u[i+1][1] and u[i+1][0]=='و': out.append(chunk+'ū'); i+=2; continue
            if v=='a' and i+1<n and not u[i+1][1] and u[i+1][0] in 'اى': out.append(chunk+'ā'); i+=2; continue
            out.append(base+(v or '')); i+=1; continue
        # konsonan
        if ch=='ل' and i==1 and u[0][0]=='ل' and KASRA in u[0][1] and KASRA in mk and i+1<n and u[i+1][0] in 'اٱ' and not any(m in u[i+1][1] for m in VOW):
            out.append('l-'); after_art=i+1; i+=1; continue
        if ch=='ل' and i==1 and u[0][0]=='ل' and (u[0][1]&set(VOW)) and not (mk&set(VOW)) :
            if SUKUN in mk:
                out.append('l-'); after_art=i+1; i+=1; continue
            if not mk and i+1<n and SHADDA in u[i+1][1] and u[i+1][0] in SUN:
                out.append(C.get(u[i+1][0])+'-'); u[i+1][1].discard(SHADDA); after_art=i+1; i+=1; continue
        s=C.get(ch)
        if s is None:
            out.append(PUNCT.get(ch,ch)); i+=1; continue
        v=vowel_of(mk)
        # hamzah awal kata tidak ditulis
        if (i==0 or i==after_art) and ch in 'أإء': s=''
        # huruf panjang berikutnya (a+ا, u+و, i+ي) digabung menjadi satu vokal panjang
        chunk=s*(2 if SHADDA in mk and s else 1)
        if DAGGER in mk: out.append(chunk+'ā'); i+=1; continue
        if v in ('a','u','i') and i+1<n and not u[i+1][1]:
            nx=u[i+1][0]
            if (v=='a' and nx in 'اى') or (v=='u' and nx=='و') or (v=='i' and nx=='ي'):
                out.append(chunk+{'a':'ā','u':'ū','i':'ī'}[v]); i+=2; continue
        out.append(chunk+(v or '')); i+=1
    return ''.join(out)

def pausal(word, latin):
    """bentuk jeda kata terakhir: ta marbutah -> h, vokal akhir pendek dihilangkan (tanwin fathatan dipertahankan)"""
    ws=split_units(word)
    if not ws: return latin
    last=ws[-1]
    marks=[x for x in last[1] if x in VOW or x in TAN]
    if last[0]=='ة':
        if marks and not any(x in TAN for x in marks): return re.sub(r't[aiu]$','h',latin)
        return latin
    if marks and not any(x in TAN for x in marks) and last[0] not in 'وياى' and latin and latin[-1] in 'aiu':
        return latin[:-1]
    return latin

def tr(text):
    """transliterasi frasa/kalimat; artikel setelah kata lain disambung (kasyful-ḥisāb); kata terakhir dibaca jeda"""
    toks=re.findall(r'[^\s؟،؛.!?]+|[؟،؛.!?]',text)
    out=[]
    for k,t in enumerate(toks):
        if t in PUNCT or t in '.!?':
            out.append(PUNCT.get(t,t)); continue
        starts = (not out) or out[-1] in ('?',',',';','.','!')
        lat=tr_word(t, first_in_phrase=starts)
        nxt_punct = (k+1>=len(toks)) or toks[k+1] in PUNCT or toks[k+1] in '.!?'
        if nxt_punct: lat=pausal(t,lat)
        if (not starts) and re.match(r'^a(l|s|sy|d|ż|t|ṡ|r|z|ṣ|ḍ|ṭ|ẓ|n)-',lat) and out and out[-1][-1:] in 'aiuāīū':
            out[-1]+=lat[1:]; continue
        if out and out[-1] not in ('?',',',';','.','!'): out.append(' '+lat)
        elif out: out.append(' '+lat)
        else: out.append(lat)
    return re.sub(r' ([?,;.!])',r'\1',''.join(out))

if __name__=='__main__':
    for s in ['حَاسُوب','شَاشَة','لَوْحَةُ الْمَفَاتِيحِ','كَشْفُ الْحِسَابِ','هَيْكَلُ السَّيَّارَةِ','رَشّ','مَوْقِع إِلِكْتُرُونِيّ','صَفْحَة رَئِيسِيَّة','مَا مُشْكِلَةُ الدَّرَّاجَةِ؟','يَحْتَاجُ إِلَى تَغْيِيرِ الزَّيْتِ','اِنْتَظِرْ قَلِيلًا مِنْ فَضْلِكَ','فَأْرَة','بِالْمِطْرَقَةِ','خَدْش','دَرَّاجَة نَارِيَّة','مِفْتَاحُ عَزْمٍ','رَأْسُ الْمَالِ','وَيْب','هٰذَا','أَسْتَخْدِمُ الْحَاسُوبَ كُلَّ يَوْمٍ','مَهْلًا، هُنَاكَ خَطَر','نَاقِلُ الْحَرَكَةِ','شَمْعَةُ الْإِشْعَالِ','مُصَفِّي الْهَوَاءِ','قَاعِدَةُ الْبَيَانَاتِ','مَسْؤُول']:
        print(s,'->',tr(s))
