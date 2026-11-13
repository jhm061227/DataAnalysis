import sys, re, pandas as pd, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
df=pd.read_excel(sys.argv[1])
df=df[df['분석제외 여부'].isna()].copy()
df=df[~df['제목'].str.contains(r'^\[?(포토|사진|인사|부고|게시판|오늘의 운세|날씨)', na=False)]
def clean(t): 
    t=re.sub(r'\[[^\]]*\]|<[^>]*>|【[^】]*】','',str(t))
    return re.sub(r'[^\w\s%.]',' ',t)
df['t']=df['제목'].map(clean)
# title char 2-3grams + top keywords
df['kw']=df['키워드'].fillna('').map(lambda s:' '.join(s.split(',')[:25]))
X1=TfidfVectorizer(analyzer='char_wb',ngram_range=(2,3),min_df=2,sublinear_tf=True).fit_transform(df['t'])
X2=TfidfVectorizer(token_pattern=r'[^ ]{2,}',min_df=2,max_df=0.05,sublinear_tf=True).fit_transform(df['kw'])
from scipy.sparse import hstack
from sklearn.preprocessing import normalize
X=normalize(hstack([X1*0.5,X2*0.5*1.0]).tocsr())
nn=NearestNeighbors(n_neighbors=15,metric='cosine').fit(X)
d,idx=nn.kneighbors(X)
par=list(range(len(df)))
def f(a):
    while par[a]!=a: par[a]=par[par[a]]; a=par[a]
    return a
TH=float(sys.argv[2]) if len(sys.argv)>2 else 0.55
for i in range(len(df)):
    for dist,j in zip(d[i],idx[i]):
        if j!=i and 1-dist>=TH: par[f(i)]=f(j)
df['c']=[f(i) for i in range(len(df))]
g=df.groupby('c').agg(n=('제목','size'),outlets=('언론사','nunique'),cat=('통합 분류1',lambda s:s.mode().iat[0] if s.notna().any() else ''),
    days=('일자',lambda s:','.join(map(str,sorted(set(s%10000)))))).sort_values('outlets',ascending=False)
df.to_pickle('/home/claude/data/clustered.pkl')
for c,r in g.head(40).iterrows():
    sub=df[df.c==c]
    print(f"\n### n={r.n} 언론사={r.outlets} {r['cat']} [{r.days}]")
    for t in sub.drop_duplicates('언론사')['제목'].head(4): print('  -',t)
