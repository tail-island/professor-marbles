<script setup>
import { ref, onMounted } from 'vue'
import TestTube from '@/components/TestTube.vue'
import { range } from '@/models/utility'

const props = defineProps(['testTubes'])

const cellSize = ref(1)

const testTubeXs = ref(Array(16).fill(1)) // マジック・ナンバーが入っちゃってごめんなさい。
const testTubeYs = ref(Array(16).fill(1)) // 同上。

const resizeObserver = new ResizeObserver(_ => {
  const width = root.value.getBoundingClientRect().width - 2
  const height = root.value.getBoundingClientRect().height - 2

  const maxTestTubeSize = Math.max(...props.testTubes.map(testTube => testTube.size))

  cellSize.value = Math.min(width / props.testTubes.length, height / maxTestTubeSize)

  testTubeXs.value = range(props.testTubes.length).map(i => i * width / props.testTubes.length + (width / props.testTubes.length - cellSize.value) / 2)
  testTubeYs.value = range(props.testTubes.length).map(i => (height - maxTestTubeSize * cellSize.value) / 2 + (maxTestTubeSize - props.testTubes[i].size) * cellSize.value)
})

const root = ref(null)

onMounted(() => {
  resizeObserver.observe(root.value)
})
</script>

<template>
  <div ref="root" class="game-board" @click="click">
    <test-tube
      v-for="(testTube, i) in testTubes"
      :key="i"
      :size="testTube.size"
      :marbles="testTube.marbles"
      :left="testTubeXs[i]"
      :top="testTubeYs[i]"
      :cellSize="cellSize"
    />
  </div>
</template>

<style>
.game-board {
  border: solid 1px #000000;
  width: 100%;
  height: 100%;
  position: relative;
}
</style>
