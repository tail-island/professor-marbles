import { CartesianProduct } from 'js-combinatorics'

export class Game {
  constructor (testTubeSizes, initialMarblesCollection, answerMarblesCollection) {
    [this.testTubes, this.answerTestTubes] = [initialMarblesCollection, answerMarblesCollection].map(marblesCollection =>
      marblesCollection.map((marbles, i) => ({ marbles: marbles, size: testTubeSizes[i] }))
    )

    this.actionCount = 0
  }

  getLegalActions () {
    return [...CartesianProduct.of(
      this.testTubes.flatMap(({ marbles }, i) => marbles.length > 0 ? i : []),
      this.testTubes.flatMap(({ marbles, size }, i) => marbles.length < size ? i : [])
    )].filter(action => action[0] !== action[1])
  }

  doAction ([from, to]) {
    while (this.testTubes[from].marbles.length > 0 && this.testTubes[to].marbles.length < this.testTubes[to].size) {
      this.testTubes[to].marbles.push(this.testTubes[from].marbles.pop())
    }

    this.actionCount++
  }

  hasFinished () {
    const testTubesToString = testTubes => `[${testTubes.map(testTube => `[${testTube.marbles.toString()}]`).toString()}]`

    return testTubesToString(this.testTubes) === testTubesToString(this.answerTestTubes)
  }
}
