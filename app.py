import random
import streamlit as st

OUTCOME_WIN = "Win"
OUTCOME_TOO_HIGH = "Too High"
OUTCOME_TOO_LOW = "Too Low"

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    #update the possible values in the input
    if value <= 0:
        return False, None, "Guess must be a positive number." #IT CAN NOT USE 0 OR NEGATIVE

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return OUTCOME_WIN, "🎉 Correct!"

    #update the comparison
    try:
        if guess < secret: 
            return OUTCOME_TOO_LOW, "📈 Go HIGHER!"
        else:
            return OUTCOME_TOO_HIGH, "📉 Go LOWER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return OUTCOME_WIN, "🎉 Correct!"
        if g > secret:
            return OUTCOME_TOO_HIGH, "📉 Go LOWER!"
        return OUTCOME_TOO_LOW, "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == OUTCOME_WIN:
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == OUTCOME_TOO_HIGH:
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == OUTCOME_TOO_LOW:
        return current_score - 5

    return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    #set by 100, later it will be subtract or just show the final score
    st.session_state.score = 100

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "outcomes" not in st.session_state:
    st.session_state.outcomes = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. " #NO MORE HARD CODE
    f"Attempts left: {(attempt_limit - 1) - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
    st.write("Range:", f"{low} to {high}") #add range based of the dificulties
    st.write("Attempt Limit:", attempt_limit) #add attempt limit based of the dificulties
    st.write("Status:", st.session_state.status) #add status based of the dificulties

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 100
    st.session_state.history = []
    st.session_state.outcomes = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    #check error if the value is higher what is the capacity
    elif guess_int > high:
        st.error(f"You get bigger than {high}.")
        #check the history, can't repeat same number
    elif guess_int in st.session_state.history:
        st.error("You already typed this number.")
    else:
        st.session_state.attempts += 1 #only work after summit and check there is not error
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)
        st.session_state.outcomes.append(outcome)

        if show_hint:
            distance = abs(guess_int - st.session_state.secret)
            range_size = high - low
            pct = distance / range_size
            if pct < 0.05:
                temp = "🔥🔥 Very Hot!"
            elif pct < 0.15:
                temp = "🔥 Hot!"
            elif pct < 0.30:
                temp = "🌡️ Warm"
            elif pct < 0.50:
                temp = "❄️ Cold"
            else:
                temp = "🧊 Freezing"
            st.warning(f"{message}  |  {temp}")

        #update the subtract operation
        st.session_state.score = st.session_state.score - (100 // attempt_limit)

        if outcome == OUTCOME_WIN:
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.sidebar.metric("Score", st.session_state.score)

if st.session_state.history:
    with st.expander("Session Summary", expanded=False):
        valid_history = [g for g in st.session_state.history if isinstance(g, int)]
        rows = []
        for i, guess in enumerate(valid_history):
            outcome = st.session_state.outcomes[i] if i < len(st.session_state.outcomes) else "-"
            if outcome == OUTCOME_WIN:
                icon = "🎉 Win"
            elif outcome == OUTCOME_TOO_HIGH:
                icon = "📈 Too High"
            elif outcome == OUTCOME_TOO_LOW:
                icon = "📉 Too Low"
            else:
                icon = outcome
            rows.append({"#": i + 1, "Guess": guess, "Result": icon})
        st.table(rows)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
