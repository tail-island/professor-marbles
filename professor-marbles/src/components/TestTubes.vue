<script setup>
import { computed, ref, onMounted } from 'vue'
import TestTube from '@/components/TestTube.vue'
import { range } from '@/models/utility'

const props = defineProps(['testTubes'])

const root = ref(null)
const width = ref(0)
const height = ref(0)

const maxTestTubeSize = computed(() => Math.max(...props.testTubes.map(testTube => testTube.size)))
const cellSize = computed(() => Math.min(width.value / props.testTubes.length, height.value / maxTestTubeSize.value))
const testTubeXs = computed(() => range(props.testTubes.length).map(i => i * width.value / props.testTubes.length + (width.value / props.testTubes.length - cellSize.value) / 2))
const testTubeYs = computed(() => range(props.testTubes.length).map(i => (height.value - maxTestTubeSize.value * cellSize.value) / 2 + (maxTestTubeSize.value - props.testTubes[i].size) * cellSize.value))

const resizeObserver = new ResizeObserver(_ => {
  width.value = root.value.getBoundingClientRect().width - 2
  height.value = root.value.getBoundingClientRect().height - 2
})

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
