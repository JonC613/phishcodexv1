import React from 'react'
import ReactDOM from 'react-dom/client'
import { FluentProvider, webLightTheme } from '@fluentui/react-components'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import App from './pages/App'
import ShowDetail from './pages/ShowDetail'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />
  },
  {
    path: '/shows/:showdate',
    element: <ShowDetail />
  }
])

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <FluentProvider theme={webLightTheme}>
      <RouterProvider router={router} />
    </FluentProvider>
  </React.StrictMode>
)
