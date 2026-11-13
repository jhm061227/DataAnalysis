import pandas as pd, re, collections, math
df=pd.read_pickle('data/clustered.pkl')
sel=[('투표지 반출·부정선거론','투표함 반출'),('조작기소 특검법','조작기소'),('윤석열 선거법 2심','당선 무효형'),
('김기현 명품가방 1심 무죄','김기현'),('수출 1조 달러 눈앞','1조 달러'),('퇴직연금 개편','퇴직'),('SK하이닉스 3분기 실적','SK하이닉스'),
('821조 예산 시정연설','821조'),('코스피 급락·사이드카','사이드카'),('가상자산 과세 유예','가상자산 과세'),('진성준 미국 비자 논란','진성준'),
('수능 AI 안경 처벌','안경'),('10월 소비자물가','소비자물가'),('주식 결제주기 단축','다음날'),('아주대 소아응급 집단사직','아주대')]
g=df.groupby('c').agg(o=('언론사','nunique'))
big=set(g[g.o>=10].index)
rows=[]
for i,(name,k) in enumerate(sel,1):
    cand=df[df['제목'].str.contains(k,na=False,regex=False)&df.c.isin(big)].c.value_counts()
    c=cand.index[0]; sub=df[df.c==c]
    for _,r in sub.iterrows(): rows.append((f'E{i:02d}',name,r['일자'],r['언론사'],r['제목'],r['키워드']))
out=pd.DataFrame(rows,columns=['eid','event','date','outlet','headline','kw'])
out.insert(0,'id',range(1,len(out)+1))
# distinctive keywords
N=len(df); dfreq=collections.Counter()
for s in df['키워드'].fillna(''): dfreq.update(set(s.split(',')))
kws={}
for e,sub in out.groupby('eid'):
    tf=collections.Counter()
    for s in sub.kw.fillna(''): tf.update(set(s.split(',')))
    sc={w:tf[w]/len(sub)*math.log(N/dfreq[w]) for w in tf if len(w)>=2 and tf[w]>=len(sub)*0.3}
    kws[e]=[w for w,_ in sorted(sc.items(),key=lambda x:-x[1])[:6]]
    print(e,sub.event.iloc[0],len(sub),sub.outlet.nunique(),kws[e])
out['keywords']=out.eid.map(lambda e:' · '.join(kws[e]))
out.drop(columns='kw').to_csv('data/pilot12.csv',index=False)
