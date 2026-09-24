import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from workplace_learning_recommender.core import recommend

resources=[{'id':'r1','skill':'python','quality':.9},{'id':'r2','skill':'writing','quality':.9}]
for item in recommend({'python':1,'writing':.2},resources):
    print(f"{item['id']}: {item['skill']} (quality={item['quality']})")
