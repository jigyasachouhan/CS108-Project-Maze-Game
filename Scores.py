
# function to read the original high scores from the file
def get_scores():
    with open("scores.txt", "r") as file :
        scores = [int(line.strip()) for line in file if line.strip() != ""]  # scores is an array which has the integer values of the high scores
    return scores

# function to check if the new score is a high score and add the new high score to the file
def add_score(score):
    scores = get_scores()
    scores.append(score)   # add the new score to the array
    scores.sort(reverse=True)    # sort the scores in decreasing order
    if len(scores) > 5:    # to handle the cases when the games played yet are less than 5 then no need to pop
        scores.pop()

    # write the high scores back into scores.txt
    with open("scores.txt", "w") as file:
        for i in range(len(scores)):
            file.write(str(scores[i]) + "\n")

