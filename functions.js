import pickRandom from 'pick-random';

function searchWord(dictionary, word, max, mode) {
    var wordsList = [];
    for (var i = 0; i < dictionary.length; i++) {
        if (dictionary[i].includes(word.toLowerCase())) {
            wordsList.push(dictionary[i]);
        }
    }
    if (mode == true) {
        return wordsList;
    }
    if (max < 0 && max > 100) {
        console.error('Max must be between 0 and 100');
        process.exit(1);
    }
    if (wordsList.length > max && max != 0) {
        wordsList = pickRandom(wordsList, { count: max });
    }
    return wordsList;
}

export {
    searchWord
};