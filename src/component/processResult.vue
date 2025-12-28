
<template>
  <div class="bg-gray-100 p-8 min-h-screen">
    <div class="max-w-6xl mx-auto">
      <h2 class="text-3xl font-bold text-center mb-8 text-gray-800">Proses Identifikasi Citra</h2>
      
      <!-- Final Result Card -->
      <div class="bg-white rounded-xl shadow-lg p-6 mb-8 text-center" :class="{'border-l-8 border-green-500': result.class === 'Fresh', 'border-l-8 border-red-500': result.class === 'Busuk'}">
        <h3 class="text-2xl font-bold mb-2" :class="{'text-green-600': result.class === 'Fresh', 'text-red-600': result.class === 'Busuk'}">
          {{ result.class === 'Fresh' ? '🥔 Kentang Segar (Fresh)' : '🦠 Kentang Busuk (Rotten)' }}
        </h3>
        <p class="text-gray-600">Akurasi Prediksi: <span class="font-bold">{{ (result.confidence * 100).toFixed(2) }}%</span></p>
      </div>

      <!-- Process Steps Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <!-- 1. Resize -->
        <div class="bg-white p-4 rounded-lg shadow transition hover:shadow-md">
           <p class="text-center font-semibold mb-2 text-gray-700">1. Resize (128x128)</p>
           <div class="aspect-square flex items-center justify-center bg-gray-50 rounded border overflow-hidden">
             <img :src="'data:image/png;base64,' + result.steps.resized" class="max-w-full max-h-full object-contain" />
           </div>
        </div>
        
        <!-- 2. Grayscale -->
        <div class="bg-white p-4 rounded-lg shadow transition hover:shadow-md">
           <p class="text-center font-semibold mb-2 text-gray-700">2. Grayscale</p>
           <div class="aspect-square flex items-center justify-center bg-gray-50 rounded border overflow-hidden">
             <img :src="'data:image/png;base64,' + result.steps.grayscale" class="max-w-full max-h-full object-contain grayscale" />
           </div>
        </div>

        <!-- 3. Gaussian Blur -->
        <div class="bg-white p-4 rounded-lg shadow transition hover:shadow-md">
           <p class="text-center font-semibold mb-2 text-gray-700">3. Gaussian Blur</p>
           <div class="aspect-square flex items-center justify-center bg-gray-50 rounded border overflow-hidden">
             <img :src="'data:image/png;base64,' + result.steps.blur" class="max-w-full max-h-full object-contain" />
           </div>
        </div>

        <!-- 4. Threshold -->
        <div class="bg-white p-4 rounded-lg shadow transition hover:shadow-md">
           <p class="text-center font-semibold mb-2 text-gray-700">4. Thresholding</p>
           <div class="aspect-square flex items-center justify-center bg-gray-50 rounded border overflow-hidden">
             <img :src="'data:image/png;base64,' + result.steps.threshold" class="max-w-full max-h-full object-contain" />
           </div>
        </div>

        <!-- 5. Contours -->
        <div class="bg-white p-4 rounded-lg shadow transition hover:shadow-md">
           <p class="text-center font-semibold mb-2 text-gray-700">5. Contour Detection</p>
           <div class="aspect-square flex items-center justify-center bg-gray-50 rounded border overflow-hidden">
             <img :src="'data:image/png;base64,' + result.steps.contours" class="max-w-full max-h-full object-contain" />
           </div>
        </div>

        <!-- 6. ROI -->
        <div class="bg-white p-4 rounded-lg shadow transition hover:shadow-md ring-2 ring-blue-100">
           <p class="text-center font-semibold mb-2 text-blue-700">6. ROI (Region of Interest)</p>
           <div class="aspect-square flex items-center justify-center bg-gray-50 rounded border overflow-hidden">
             <img :src="'data:image/png;base64,' + result.steps.roi" class="max-w-full max-h-full object-contain" />
           </div>
        </div>
      </div>

      <!-- Features Table -->
      <div class="bg-white rounded-xl shadow p-6">
        <h4 class="text-xl font-bold mb-4 text-gray-800">Ekstraksi Fitur (GLCM & Shape)</h4>
        <div class="overflow-x-auto">
          <table class="min-w-full text-sm text-left text-gray-500">
             <thead class="text-xs text-gray-700 uppercase bg-gray-50">
                <tr>
                   <th class="px-6 py-3">Fitur</th>
                   <th class="px-6 py-3">Nilai</th>
                   <th class="px-6 py-3">Deskripsi</th>
                </tr>
             </thead>
             <tbody>
                <!-- GLCM Features -->
                <tr class="bg-white border-b">
                   <td class="px-6 py-4 font-medium text-gray-900">Contrast</td>
                   <td class="px-6 py-4">{{ result.features.Contrast ? result.features.Contrast.toFixed(2) : 0 }}</td>
                   <td class="px-6 py-4">Perbedaan intensitas piksel</td>
                </tr>
                <tr class="bg-white border-b">
                   <td class="px-6 py-4 font-medium text-gray-900">Dissimilarity</td>
                   <td class="px-6 py-4">{{ result.features.Dissimilarity ? result.features.Dissimilarity.toFixed(2) : 0 }}</td>
                   <td class="px-6 py-4">Variasi pasangan piksel</td>
                </tr>
                <tr class="bg-white border-b">
                   <td class="px-6 py-4 font-medium text-gray-900">Homogeneity</td>
                   <td class="px-6 py-4">{{ result.features.Homogeneity ? result.features.Homogeneity.toFixed(4) : 0 }}</td>
                   <td class="px-6 py-4">Keseragaman tekstur</td>
                </tr>
                <tr class="bg-white border-b">
                    <td class="px-6 py-4 font-medium text-gray-900">Energy</td>
                    <td class="px-6 py-4">{{ result.features.Energy ? result.features.Energy.toFixed(4) : 0 }}</td>
                    <td class="px-6 py-4">Keseragaman distribusi</td>
                 </tr>
                 <tr class="bg-white border-b">
                    <td class="px-6 py-4 font-medium text-gray-900">Correlation</td>
                    <td class="px-6 py-4">{{ result.features.Correlation ? result.features.Correlation.toFixed(4) : 0 }}</td>
                    <td class="px-6 py-4">Ketergantungan linier</td>
                 </tr>

                 <!-- Shape Features -->
                 <tr class="bg-gray-50 border-b">
                    <td colspan="3" class="px-6 py-2 font-bold text-gray-700 bg-blue-50">Fitur Bentuk (Shape)</td>
                 </tr>
                 <tr class="bg-white border-b">
                    <td class="px-6 py-4 font-medium text-gray-900">Area</td>
                    <td class="px-6 py-4">{{ result.features.Area ? result.features.Area.toFixed(0) : 0 }}</td>
                    <td class="px-6 py-4">Luas area objek (pixel)</td>
                 </tr>
                 <tr class="bg-white border-b">
                    <td class="px-6 py-4 font-medium text-gray-900">Perimeter</td>
                    <td class="px-6 py-4">{{ result.features.Perimeter ? result.features.Perimeter.toFixed(2) : 0 }}</td>
                    <td class="px-6 py-4">Keliling objek</td>
                 </tr>
                 <tr class="bg-white border-b">
                    <td class="px-6 py-4 font-medium text-gray-900">Circularity</td>
                    <td class="px-6 py-4">{{ result.features.Circularity ? result.features.Circularity.toFixed(4) : 0 }}</td>
                    <td class="px-6 py-4">Kebulatan (1 = Lingkaran Sempurna)</td>
                 </tr>
                 <tr class="bg-white">
                    <td class="px-6 py-4 font-medium text-gray-900">Aspect Ratio</td>
                    <td class="px-6 py-4">{{ result.features.AspectRatio ? result.features.AspectRatio.toFixed(4) : 0 }}</td>
                    <td class="px-6 py-4">Rasio Lebar : Tinggi</td>
                 </tr>
             </tbody>
          </table>
        </div>
      </div>

      <div class="mt-8 text-center">
        <button @click="$emit('back')" class="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition">
           &larr; Scan Gambar Lain
        </button>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  props: {
    result: {
      type: Object,
      required: true
    }
  }
}
</script>
