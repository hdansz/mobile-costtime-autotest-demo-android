#encoding utf-8
from Tools import compimgs_similar
import os

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    p1 = path + "/temp_screenshot/" + "test.jpg"
    p2 = path + "/expected_resultimg/" + "except.jpg"
    compimgs_similar.runImgSimilar(p1, p2)