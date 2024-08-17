# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
dic = {}
def player(prev_play, opponent_history=[]):
  opponent_history.append(prev_play)
  guess = "S"
  if len(opponent_history)>6:
    a = "".join(opponent_history[-6:])
    if "".join(opponent_history[-7:]) in dic.keys():
      dic["".join(opponent_history[-7:])]+=1
    b1 = a+"R"
    b2 = a+"P"
    b3 = a+"S"
    b = [b1,b2,b3]
    for i in b:
      dic[i] = dic.get(i, 0)
    f = max(b, key=lambda key: dic[key])
    guess = {"R": "P", "P": "S", "S": "R"}[f[-1]]
  return guess