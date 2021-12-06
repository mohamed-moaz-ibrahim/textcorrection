from textcorrection import SPELLING

#initializing object 
corrector = SPELLING(number_of_suggestion_result = 2, number_of_letters_to_transform = 1,
 char_deleting=True, char_inserting=True, char_replacing=True, char_swaping=True, verbose= False)

#creating word pool from your data file
corrector.create_words_pool_from_text_file('data/medical_vocab.txt', 'abcdefghijklmnopqrstuvwxyz')
# corrector.create_words_pool_from_text('ai ai and ai ai ai ai machine learning class at epsilon ai institute', 'abcdefghijklmnopqrstuvwxyz')
# corrector.create_words_pool_from_json('data/egyption_arabic.json','ابتثجحخدذرزسشصضطظعغفقكلمنويءؤئإألإ')
top_suggestions = corrector.get_most_frequent(input("type something ..: \n"))
for i in range(len(top_suggestions)):
    print(f'suggestion number {i+1} is: {top_suggestions[i]}')