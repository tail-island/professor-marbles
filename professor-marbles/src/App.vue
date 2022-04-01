<script setup>
import { onMounted, ref } from 'vue'
import { Game } from '@/models/game'
import { range } from '@/models/utility'
import TestTubes from '@/components/TestTubes.vue'

const game = ref(new Game([], [], []))
const errorMessage = ref('')
const questionTextArea = ref(null)
const answerTextArea = ref(null)

const execute = () => {
  const [testTubeSizes, initialMarblesCollection, answerMarblesCollection] = (() => {
    const lines = questionTextArea.value.value.trim().split(/\n/)
    let lineNumber = 0

    const testTubeCount = parseInt(lines[lineNumber++])

    return [
      range(testTubeCount).map(_ => parseInt(lines[lineNumber++])),
      range(testTubeCount).map(_ => {
        const line = lines[lineNumber++]

        return line !== '' ? line.split(/ /).map(s => parseInt(s, 16)) : []
      }),
      range(testTubeCount).map(_ => {
        const line = lines[lineNumber++]

        return line !== '' ? line.split(/ /).map(s => parseInt(s, 16)) : []
      })
    ]
  })()

  game.value = new Game(testTubeSizes, initialMarblesCollection, answerMarblesCollection)

  const actions = answerTextArea.value.value.trim().split(/\n/).map(line => line.split(/ /).map(s => parseInt(s)))
  const interval = Math.max(100, Math.min(1000, 10000 / actions.length))

  setTimeout(function doAction (i) {
    if (i >= actions.length) {
      return
    }

    if (game.value.getLegalActions().every(legalAction => legalAction.toString() !== actions[i].toString())) {
      errorMessage.value = `解答の${i + 1}行目が不正です。`
      return
    }

    game.value.doAction(actions[i])

    setTimeout(doAction, interval, i + 1)
  }, interval, 0)
}

onMounted(() => {
  questionTextArea.value.value = '4\n4\n2\n4\n2\n18 7a 7a 07\n18\n07\n18 07\n07 7a 18 18\n07 18\n\n07 7a'
  answerTextArea.value.value = '0 1\n1 2\n0 1\n3 0\n2 3\n1 2\n3 2\n0 3\n0 1\n2 0\n3 2\n0 3\n2 0'
})
</script>

<template>
  <div class="title">
    ビーダマ教授
  </div>
  <div class="question">
    <textarea ref="questionTextArea"></textarea>
  </div>
  <div class="goal">
    <TestTubes :testTubes="game.answerTestTubes" />
  </div>
  <div class="answer">
    <textarea ref="answerTextArea">answer</textarea>
  </div>
  <div class="command">
    <button @click="execute">実行</button>
  </div>
  <div class="board">
    <TestTubes :testTubes="game.testTubes" />
  </div>
  <div class="status">
    count: {{ game.actionCount }}&nbsp;&nbsp;<span class="error">{{ errorMessage }}</span>
  </div>
</template>

<style>
#app {
  display: grid;
  grid-template-columns: 1fr 320px 1fr;
  grid-template-rows: 32pt 320px 32pt 1fr 32pt;
  height: 100%;
}

#app > * {
  margin: 0;
  padding: 8px;
}

.title {
  grid-column: 1 / 4;
  grid-row: 1;
  overflow: hidden;
  text-align: center;
}

.question {
  grid-column: 1;
  grid-row: 2;
}

.goal {
  grid-column: 2;
  grid-row: 2;
}

.answer {
  grid-column: 3;
  grid-row: 2;
}

.question > *, .answer > * {
  box-sizing: border-box;
  height: 100%;
  width: 100%;
}

.command {
  text-align: center;
  grid-column: 1 / 4;
  grid-row: 3;
}

.board {
  grid-column: 1 / 4;
  grid-row: 4;
}

.status {
  grid-column: 1 / 4;
  grid-row: 5;
  text-align: center;
}

.error {
  color: #ff0000;
}
</style>
