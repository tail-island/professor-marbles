<script setup>
import { range } from '@/models/utility'
import TestTubeCell from '@/components/TestTubeCell.vue'

defineProps(['size', 'marbles', 'left', 'top', 'cellSize'])
</script>

<template>
  <div class="test-tube" v-bind:style="{left: `${left}px`, top: `${top}px`}">
    <TestTubeCell
      v-for="i in range(size)"
      :key="i"
      :marble="size - 1 - i >= marbles.length ? -1 : marbles[size - 1 - i]"
      :size="cellSize"
    />
  </div>
</template>

<style>
.test-tube {
  position: absolute;
}
</style>
