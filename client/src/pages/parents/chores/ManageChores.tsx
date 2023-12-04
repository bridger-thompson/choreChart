import { useState } from "react";
import { FilterTextRow } from "../../../components/forms/FilterTextRow";
import { Spinner } from "../../../components/ui/Spinner";
import { ChoreEditorModal } from "./ChoreEditorModal";
import { ChoreRow } from "./ChoreRow";
import { useGetChoresQuery } from "./manageChoresHooks";

export const ManageChores = () => {
  const choresQuery = useGetChoresQuery();
  const chores = choresQuery.data ?? []
  const [filter, setFilter] = useState("")

  if (choresQuery.isLoading) return <Spinner />
  if (choresQuery.isError) return <h3 className="text-center">Error getting chores</h3>

  const filteredChores = chores.filter(c => c.name.toLowerCase().includes(filter.toLowerCase()))

  return (
    <>
      <div className="row my-1">
        <div className="col">
          <FilterTextRow
            changeHandler={(e) => setFilter(e)}
            value={filter}
            labelCol="col-xl-4 col-lg-3 col-md-2 col-3"
            inputCol="col-md col" />
        </div>
        <div className="col-2 text-end">
          <ChoreEditorModal />
        </div>
      </div>
      <div className="list-group rounded-5">
        {filteredChores.map((c) => (
          <div key={c.id} className="list-group-item bg-transparent frosted-glass">
            <ChoreRow chore={c} />
          </div>
        ))}
      </div>
    </>
  )
}
