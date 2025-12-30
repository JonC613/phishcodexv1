import { useEffect, useRef, useState } from 'react'
import axios from 'axios'
import {
  Button,
  Dropdown,
  Option,
  Input,
  Title3,
  Spinner,
  makeStyles,
  Caption1,
  Divider
} from '@fluentui/react-components'
import ShowCard from '../components/ShowCard'
import { PaginatedShows, ShowCard as ShowCardType } from '../types/api'

const useStyles = makeStyles({
  container: { maxWidth: '900px', margin: '0 auto', padding: '24px' },
  controls: { display: 'flex', gap: '8px', marginBottom: '12px', flexWrap: 'wrap' }
})

const searchKinds = ['recent', 'date', 'year', 'venue', 'city', 'state', 'country']

export default function App() {
  const styles = useStyles()
  const [kind, setKind] = useState('recent')
  const [query, setQuery] = useState('')
  const [shows, setShows] = useState<ShowCardType[]>([])
  const [cursor, setCursor] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const sentinelRef = useRef<HTMLDivElement | null>(null)

  const fetchShows = async (reset = false) => {
    setLoading(true)
    const params: any = { kind }
    if (query) params.q = query
    if (!reset && cursor) params.cursor = cursor
    const res = await axios.get<PaginatedShows>('/api/search', { params })
    setShows((prev) => (reset ? res.data.items : [...prev, ...res.data.items]))
    setCursor(res.data.next_cursor)
    setLoading(false)
  }

  useEffect(() => {
    fetchShows(true)
  }, [])

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      const [entry] = entries
      if (entry.isIntersecting && cursor && !loading) {
        fetchShows()
      }
    })
    const node = sentinelRef.current
    if (node) observer.observe(node)
    return () => {
      if (node) observer.unobserve(node)
    }
  }, [cursor, loading])

  const onSearch = () => {
    setCursor(null)
    fetchShows(true)
  }

  return (
    <div className={styles.container}>
      <Title3>Phish Show Finder</Title3>
      <div className={styles.controls}>
        <Dropdown selectedOptions={[kind]} onOptionSelect={(_, data) => setKind(data.optionValue as string)}>
          {searchKinds.map((k) => (
            <Option key={k} value={k}>
              {k}
            </Option>
          ))}
        </Dropdown>
        <Input placeholder="Search" value={query} onChange={(_, data) => setQuery(data.value)} />
        <Button appearance="primary" onClick={onSearch}>
          Search
        </Button>
      </div>
      <Caption1>Showing {shows.length} results</Caption1>
      <Divider style={{ margin: '12px 0' }} />
      {shows.map((s) => (
        <ShowCard key={`${s.showdate}-${s.showid}`} show={s} />
      ))}
      {loading && <Spinner label="Loading" />}
      <div ref={sentinelRef} style={{ height: 20 }} />
    </div>
  )
}
