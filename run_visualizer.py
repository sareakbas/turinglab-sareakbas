from turinglab.tm_engine import SingleTapeTM
from turinglab.visualizer import TMVisualizer


tm = SingleTapeTM.from_yaml("machines/student_choice.yaml")
viz = TMVisualizer(tm)

# "1100" sayısının 4'e bölünebilirliğini test ederken kare kare çizecek
viz.run_and_create_gif("1100")