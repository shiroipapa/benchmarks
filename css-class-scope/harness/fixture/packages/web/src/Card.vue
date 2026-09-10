<template>
  <article class="pricing-card">
    <div class="pricing-card__price">{{ price }}</div>
    <ul class="pricing-card__features">
      <li v-for="f in features" :key="f">{{ f }}</li>
    </ul>
    <a class="ds-button ds-button--primary" href="/signup">Choose</a>
  </article>
</template>

<script setup>
defineProps({ price: String, features: Array });
</script>

<style scoped>
.card-footer {
  margin-top: 1rem;
}
</style>
