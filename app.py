from flask import Flask, jsonify, request
# initialize our Flask application
app= Flask(__name__)

@app.route("/song", methods=["GET"])
def setName():
    if request.method=='GET':
        artist = request.args.get('artist').lower()
        
        if artist=="taylor swift":
            songs = ["Shake It Off", "You Belong With Me", "Blank Space", "Love Story", "I Knew You Were Trouble."]
        
        elif artist=="eminem":
            songs = ["Superman", "Lose Yourself", "Venom", "Rap God", "Without Me"]

        elif artist=="ed sheeran":
            songs = ["Shape of You", "Bad Habits", "Perfect", "Castle on the Hill", "Galway Girl"]

        elif artist=="sia":
            songs = ["Unstoppable", "Genius", "Chandelier", "The Greatest", "I'm Still Here"]

        elif artist=="akon":
            songs = ["Chammak Challo", "Smack That", "I Wanna Love You", "Beautiful", "Lonely"]

        elif artist=="linkin park":
            songs = ["Numb", "Faint", "New Divide", "In the End", "Breaking the Habit"]

        elif artist=="metallica":
            songs = ["Enter Sandman", "One", "Master of Puppets", "For Whom The Bell Tolls", "Fade to Black"]

        elif artist=="harry styles":
            songs = ["As It Was", "Watermelon Sugar"]
        
        else:
            songs = "No Suggestions for the arist provided"
        
        return jsonify({"songs":songs})

if __name__=='__main__':
    app.run()