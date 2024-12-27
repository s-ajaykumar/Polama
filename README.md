# Polama - Your cab booking assistant


## Description:
It is a voice to voice AI cab booking assistant.
It helps the user by asking cab booking details, confirms the exact locations, calculates the fare and books itself for the user.

## Working:
It involves 3 llm's. (Speech-to-Text, Text-to-Text, Text-to-Speech)
gemma2:2b is used as the text to text llm

## Working_pad:
ShortTerm_Goal1:
- Want Text to Text model that follows the instruction perfectly and also with faster inference.
Results:
- Identified gemma2:2b follows the instruction perfectly and also faster inference with 2-3 seconds.
- Worked in the prompt engineering for 1-2 weeks. Identified the best prompt by refining the prompt iteratively. The prompt is in the prompts.py file.

ShortTerm_Goal2:
- Want a good Speech to text model that recognizes the speech to some good accuracy.
Results:
- For now, using a proprietary model with free subscription - deepgram nova and it's nice.
- After accomplishing the Text to Text goal successfully, may research in this more deeply.

ShortTerm_Goal3:
- Same as ShortTerm_Goal2.
Results:
- Want to research once ShortTerm_Goal1 is accomplished.