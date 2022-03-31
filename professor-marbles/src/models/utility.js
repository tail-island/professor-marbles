export function * rangeGenerator (size) {
  for (let i = 0; i < size; ++i) {
    yield i
  }
}

export function range (size) {
  return [...rangeGenerator(size)]
}
