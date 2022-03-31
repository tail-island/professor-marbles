<script setup>
import { ref } from 'vue'
import { Game } from '@/models/game'
import TestTubes from '@/components/TestTubes.vue'

const game = ref(new Game([1, 2, 3, 4, 5], [[0x01], [0x23], [0x45, 0x67, 0x45], [0x89, 0xab], [0xcd, 0xef]], [[0x01], [0x23, 0x45], [0x45, 0x67], [0x89, 0xab], [0xcd, 0xef]]))

const intervalId = setInterval(() => {
  if (game.value.hasFinished()) {
    clearInterval(intervalId)
  }

  const actions = game.value.getLegalActions()
  game.value.doAction(actions[Math.floor(Math.random() * actions.length)])
}, 1000)
</script>

<template>
  <div class="title">
    ビーダマ教授
  </div>
  <div class="question">
    <textarea>question</textarea>
  </div>
  <div class="goal">
    <TestTubes :testTubes="game.answerTestTubes" />
  </div>
  <div class="answer">
    <textarea>answer</textarea>
  </div>
  <div class="command">
    <button>実行</button>
  </div>
  <div class="board">
    <TestTubes :testTubes="game.testTubes" />
  </div>
  <div class="status">
    count: {{ game.actionCount }}
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
</style>
