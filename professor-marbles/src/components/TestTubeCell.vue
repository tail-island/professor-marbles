<script>
import { computed, onMounted, ref } from 'vue'

const MARBLE_COLORS = [ // ビーダマは256色までですけど、それだと見分けづらそうなので左右に分けて16×16色とします。
  '#000000', '#808080', '#c0c0c0', '#ffffff',
  '#0000ff', '#000080', '#008080', '#008000',
  '#00ff00', '#00ffff', '#ffff00', '#ff0000',
  '#ff00ff', '#808000', '#800080', '#800000'
]
</script>

<script setup>
const props = defineProps(['marble', 'size'])

const root = ref(null)
const labelVisibility = ref('visible')

const marbleLeft = computed(() => props.marble >> 4)
const marbleRight = computed(() => props.marble & 0xf)

const resizeObserver = new ResizeObserver(_ => {
  labelVisibility.value = root.value.getBoundingClientRect().height > 32 ? 'visible' : 'hidden'
})

onMounted(() => {
  resizeObserver.observe(root.value)
})
</script>

<template>
  <div ref="root" class="test-tube-cell" v-bind:style="{width: `${size}px`, height: `${size}px`}">
    <div class="marble left" v-if="marble >= 0" v-bind:style="{backgroundColor: MARBLE_COLORS[marbleLeft]}">
      <span v-bind:style="{color: MARBLE_COLORS[marbleLeft], visibility: labelVisibility}">{{ marbleLeft.toString(16) }}</span>
    </div>
    <div class="marble right" v-if="marble >= 0" v-bind:style="{backgroundColor: MARBLE_COLORS[marbleRight]}">
      <span v-bind:style="{color: MARBLE_COLORS[marbleRight], visibility: labelVisibility}">{{ marbleRight.toString(16) }}</span>
    </div>
  </div>
</template>

<style>
  .test-tube-cell {
    box-sizing: border-box;
    border: 1px solid #008080;
    display: flex;
  }

  .marble {
    border: 1px solid #808080;
    box-sizing: border-box;
    height: 100%;
    position: relative;
    width: 50%;
  }

  .left {
    border-radius: 9999px 0 0 9999px;
  }

  .right {
    border-radius: 0 9999px 9999px 0;
  }

  .marble span {
    filter: invert(100%) grayscale(100%) contrast(100);
    font-size: 10.5pt;
    left: 50%;
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
  }
</style>
