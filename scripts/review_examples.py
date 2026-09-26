"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from workplace_learning_recommender import core
outputs={'weighted score: .6×.8 + .4×.5': .6*.8+.4*.5, 'gap coverage: current 2 to 3 of target 4': (3-2)/(4-2)}
result={'kind':'illustrative_calculation','note':'Two-component illustration only; production ranking has ten components.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
